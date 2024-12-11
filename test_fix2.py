import unittest
from unittest.mock import patch, MagicMock
import fix2

class TestFix2(unittest.TestCase):

    @patch('fix2.initialize_driver')
    @patch('fix2.navigate_to_forum')
    @patch('fix2.set_posts_per_page')
    @patch('fix2.handle_pagination')
    def test_main(self, mock_handle_pagination, mock_set_posts_per_page, mock_navigate_to_forum, mock_initialize_driver):
        # Mock the driver
        mock_driver = MagicMock()
        mock_initialize_driver.return_value = mock_driver

        # Mock the forums list
        fix2.forums = [
            {'forum_number': 1, 'forum_id': 'forum1'},
            {'forum_number': 2, 'forum_id': 'forum2'}
        ]

        # Call the main function
        fix2.main()

        # Assertions to ensure the functions were called with expected arguments
        self.assertEqual(mock_initialize_driver.call_count, 1)
        self.assertEqual(mock_navigate_to_forum.call_count, 2)
        self.assertEqual(mock_set_posts_per_page.call_count, 2)
        self.assertEqual(mock_handle_pagination.call_count, 2)

        # Ensure driver.quit() is called
        mock_driver.quit.assert_called_once()

if __name__ == "__main__":
    unittest.main()