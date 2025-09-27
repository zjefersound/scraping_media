# main.py
from utils import tools
from scraping import *
import argparse


def main():
    
    parser = argparse.ArgumentParser(
                        prog='Scraping Media Tool',
                        description='Scrape info from social media',
                        epilog='See readme file or the files because they are very simple to read, settings must be in a settings.json file'
                        )

    parser.add_argument('--youtube', '-y', type=str, help='Youtube id or username with "@"')
    parser.add_argument('--x', '-x', type=str, help='X username in the url')
    parser.add_argument('--instagram', '-i', type=str, help='Instagram username with "@" in the url')
    parser.add_argument('--tiktok', '-t', type=str, help='Tiktok username with "@"')
    parser.add_argument('--clear', action='store_true', help='clear dist dict')
    
    parser.add_argument('--save_imgs', action='store_true', help='Save the imgs and make bs64 file')

    args = parser.parse_args()
    
    if args.clear:
        tools.rm_dir('dist/')
    
    tools.make_dir('dist')
    
    print("Running...")
    if args.youtube:
        key = tools.read_settings('env.json').get('yt_api_key')
        youtube = Youtube(key)
        if args.save_imgs:
            youtube.get(args.youtube, type='bs64')
        else:
            youtube.get(args.youtube, type='clean')
        youtube.save(args.youtube)
    if args.instagram:
        instagram = Instagram()
        if args.save_imgs:
            instagram.get(args.instagram, type='bs64')
        else:
            instagram.get(args.instagram, type='clean')
        instagram.save(args.instagram)
    if args.tiktok:
        tiktok = Tiktok()
        if args.save_imgs:
            tiktok.get(args.tiktok, type='bs64')
        else:
            tiktok.get(args.tiktok, type='clean')
        tiktok.save()
    if args.x:
        x = X()
        if args.save_imgs:
            x.get(args.x, type='bs64')
        else:
            x.get(args.x, type='clean')
        x.save()
    
    

if __name__ == "__main__":
    main()
