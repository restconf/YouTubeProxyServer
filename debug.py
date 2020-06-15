from src import pytube_patch
import pytube
#
# if __name__ == "__main__":
#     pytube.__main__.apply_descrambler = pytube_patch.apply_descrambler
#     yt = pytube.YouTube(f"https://www.youtube.com/watch?v=aatr_2MstrI")
#     with open("streams.txt", "w") as f:
#         f.write(yt.streams.get_by_itag(248).url)
#         f.write(yt.streams.get_by_itag(251).url)