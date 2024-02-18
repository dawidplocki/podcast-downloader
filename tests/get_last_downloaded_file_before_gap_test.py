from random import shuffle
import unittest

from podcast_downloader.downloaded import get_last_downloaded_file_before_gap


class TestGetLastDownloadedFileBeforeGap(unittest.TestCase):
    def test_should_return_none_for_empty_collections(self):
        # Act
        result = get_last_downloaded_file_before_gap([], [])

        # Assert
        self.assertIsNone(result, "On empty directory should be return None")

    def test_should_return_none_for_empty_directory_files(self):
        # Assign
        feed_files = [
            "podcast_episode_1.mp3",
            "podcast_episode_2.mp3",
            "podcast_episode_3.mp3",
            "podcast_episode_4.mp3",
        ]

        # Act
        result = get_last_downloaded_file_before_gap(feed_files, [])

        # Assert
        self.assertIsNone(result, "On empty directory should be return None")

    def test_should_return_last_for_nonempty_directory_files(self):
        # Assign
        feed_files = [
            "podcast_episode_1.mp3",
            "podcast_episode_2.mp3",
            "podcast_episode_3.mp3",
            "podcast_episode_4.mp3",
        ]

        directory_files = feed_files.copy()

        # Act
        result = get_last_downloaded_file_before_gap(feed_files, directory_files)

        # Assert
        self.assertEqual(
            result, feed_files[-1], "Should return the last files from the feed"
        )

    def test_should_return_last_according_the_feed_order(self):
        # Assign
        feed_files = [
            "podcast_episode_1.mp3",
            "podcast_episode_2.mp3",
            "podcast_episode_3.mp3",
            "podcast_episode_4.mp3",
        ]

        directory_files = feed_files[0:-1]
        shuffle(directory_files)
        directory_files = directory_files[:1] + [feed_files[-1]] + directory_files[1:]

        # Act
        result = get_last_downloaded_file_before_gap(feed_files, directory_files)

        # Assert
        self.assertEqual(
            result, feed_files[-1], "Should return the last files from the feed"
        )