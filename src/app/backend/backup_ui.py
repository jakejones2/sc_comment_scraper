class UI:
    @staticmethod
    def print_data(comments_list, timestamps_list, datetimes_list):
        while True:
            query = input(
                """
Enter 'C', 'T', 'D' for full list of comments, timestamps, and datetimes respectively.
Press 'L' to view comments individually.
Press 'Q' to quit.
"""
            )
            if query in ("L", "l"):
                for counter, comment in enumerate(comments_list):
                    print(
                        f"""{comment}
{timestamps_list[counter]}
{datetimes_list[counter]}
_____"""
                    )
            elif query in ("C", "c"):
                for comment in comments_list:
                    print(comment)
            elif query in ("T", "t"):
                for timestamp in timestamps_list:
                    print(timestamp)
            elif query in ("D", "d"):
                for datetime in datetimes_list:
                    print(datetime)
            elif query in ("Q", "q"):
                quit()
