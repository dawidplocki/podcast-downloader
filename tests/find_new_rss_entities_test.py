import unittest

from podcast_downloader.rss import only_new_entities
from commons import rss_entity_generator


class TestFindNewRSSEntities(unittest.TestCase):
    def test_find_all_new_rss_entities(self):
        # Assign
        new_one_1, new_one_2, old_one_1, old_one_2, old_one_3 = rss_entity_generator(
            limit=5
        )
        rss_entities = [new_one_1, new_one_2, old_one_1, old_one_2, old_one_3]
        last_downloaded_file = "[20200108] file0003.mp3"

        expected = [new_one_1, new_one_2]

        # Act
        result = list(only_new_entities(last_downloaded_file, rss_entities))

        # Assert
        self.assertSequenceEqual(
            result, expected, "A both new entity should be return as result"
        )
