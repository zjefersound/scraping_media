# main.py
from utils import tools
from scraping import *
import argparse




def main():
    key = tools.read_settings('env.json').get('apikey')
    
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
    
    if args.youtube:
        obj = Youtube(key)
        if args.save_imgs:
            obj.get(args.youtube, type='bs64')
        else:
            obj.get(args.youtube, type='clean')
        obj.save()
    if args.instagram:
        obj = Instagram()
        if args.save_imgs:
            obj.get(args.instagram, type='bs64')
        else:
            obj.get(args.instagram, type='clean')
        obj.save()
    if args.tiktok:
        obj = Tiktok()
        if args.save_imgs:
            obj.get(args.tiktok, type='bs64')
        else:
            obj.get(args.tiktok, type='clean')
        obj.save()
    if args.x:
        obj = X()
        if args.save_imgs:
            obj.get(args.x, type='bs64')
        else:
            obj.get(args.x, type='clean')
        obj.save()
    
    

if __name__ == "__main__":
    main()
