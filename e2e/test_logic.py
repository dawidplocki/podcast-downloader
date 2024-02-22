from itertools import chain
from typing import Callable, Dict
from e2e.fixures import (
    FeedBuilder,
    PodcastDirectory,
    run_podcast_downloader,
    # fixures:
    download_destination_directory,
    feed,
    use_config,
    podcast_directory,
)
from e2e.random import call_n_times, generate_random_mp3_file, generate_random_string


def test_configuration_hierarchy(
    feed: FeedBuilder,
    use_config: Callable[[Dict], None],
    podcast_directory: PodcastDirectory,
):
    # Arrange
    feed.add_random_entries()

    use_config(
        {
            "if_directory_empty": "download_all_from_feed",
            "podcasts": [
                {
                    "name": generate_random_string(),
                    "path": podcast_directory.path(),
                    "rss_link": feed.get_feed_url(),
                    "if_directory_empty": "download_last",
                }
            ],
        }
    )

    # Act
    run_podcast_downloader()

    # Assert
    assert len(podcast_directory.get_files_list()) == 1


def test_ignore_files_not_being_part_of_the_feed(
    feed: FeedBuilder,
    use_config: Callable[[Dict], None],
    podcast_directory: PodcastDirectory,
):
    # Arrange
    feed.add_random_entries()
    not_podcasts_files = call_n_times(generate_random_mp3_file)
    for file_name in not_podcasts_files:
        podcast_directory.add_file(file_name)

    last_podcast_file = generate_random_mp3_file()
    feed.add_entry(file_name=last_podcast_file)

    use_config(
        {
            "podcasts": [
                {
                    "if_directory_empty": "download_last",
                    "path": podcast_directory.path(),
                    "rss_link": feed.get_feed_url(),
                }
            ],
        }
    )

    # Act
    run_podcast_downloader()

    # Assert
    podcast_directory.is_containing_only(
        [file_name.lower() for file_name in not_podcasts_files]
        + [last_podcast_file.lower()]
    )


def test_configuration_during_filling_up_gaps_should_not_download_existing_files(
    feed: FeedBuilder,
    use_config: Callable[[Dict], None],
    podcast_directory: PodcastDirectory,
):
    # Arrange
    files_downloaded_and_removed = call_n_times(generate_random_mp3_file)
    downloaded_files_before_gap = call_n_times(generate_random_mp3_file)
    files_in_the_gap = call_n_times(generate_random_mp3_file)
    downloaded_files_after_gap = call_n_times(generate_random_mp3_file)
    files_to_download = call_n_times(generate_random_mp3_file)

    for file_name in chain(
        files_downloaded_and_removed,
        downloaded_files_before_gap,
        files_in_the_gap,
        downloaded_files_after_gap,
        files_to_download,
    ):
        feed.add_entry(file_name)

    for file_name in chain(
        downloaded_files_before_gap,
        downloaded_files_after_gap,
    ):
        podcast_directory.add_file(file_name)

    use_config(
        {
            "podcasts": [
                {
                    "path": podcast_directory.path(),
                    "rss_link": feed.get_feed_url(),
                    "fill_up_gaps": True,
                }
            ],
        }
    )

    # Act
    run_podcast_downloader()

    # Assert
    assert set(feed.get_requested_files_list()) == set(files_to_download)
