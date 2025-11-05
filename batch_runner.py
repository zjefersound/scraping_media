import csv
import os
from scraping import Youtube, Instagram, Tiktok, X
from utils import tools


def run_batch(usernames, strategy, save_imgs=False, export_csv=True):
    tools.make_dir("dist")

    if strategy == "y":
        key = tools.read_settings("env.json").get("yt_api_key")
        scraper = Youtube(key)
        platform = "youtube"
    elif strategy == "i":
        scraper = Instagram()
        platform = "instagram"
    elif strategy == "t":
        scraper = Tiktok()
        platform = "tiktok"
    elif strategy == "x":
        scraper = X()
        platform = "x"
    else:
        raise ValueError(f"Invalid strategy '{strategy}', must be one of 'y', 'i', 't', 'x'")

    csv_path = os.path.join("dist", "dataset_real.csv")

    # Cabeçalho do CSV (apenas se for o primeiro arquivo)
    if export_csv and not os.path.exists(csv_path):
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "platform", "username", "name", "desc", "country", "followers",
                "post_id", "title", "views", "likes", "comments", "favorites", "date"
            ])

    for username in usernames:
        if not len(username):
            continue
        try:
            print(f"Running for {username} with strategy '{strategy}'...")

            data = scraper.get(username, type="clean" if not save_imgs else "bs64")
            scraper.save(username)

            if export_csv and data:
                profile = data.get("profile", {})
                posts = data.get("posts", [])

                for post in posts:
                    with open(csv_path, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            platform,
                            profile.get("username"),
                            profile.get("name"),
                            profile.get("desc"),
                            profile.get("country"),
                            profile.get("stats", {}).get("followers"),
                            post.get("id"),
                            post.get("title"),
                            post.get("stats", {}).get("views"),
                            post.get("stats", {}).get("likes"),
                            post.get("stats", {}).get("comments"),
                            post.get("stats", {}).get("favorites"),
                            post.get("date"),
                        ])

        except Exception as e:
            print(f"ERROR with: {username} - Skipping... ({e})")
            continue

if __name__ == "__main__":
    usernames = [
            # "@JoojNatu",
            # "@triplecharm",
            # "@ryan_samuel8",
            # "@emozgaming",
            # "@GrimShorts",
            # "@julseyhiphop",
            # "@SwiftieTikToks",
            # "@realjulianbanks",
            # "@iiNoodleDoodleii",
            # "@GLArt",
            # "@art.tik.25",
            # "@meredithduxbury",
            # "@glambby_",
            # "@marinetta27",
            # "@oCastrin",
            # "@PMM",
            # "@Dance_up_",
            # "@Jazzghost",
            # "@kikakimm",
            # "@ashleymanzano",
            # "@Isseymoloney",
            # "@yinicorn",
            # "@nicolylarissa",
            # "@Thatstudygirl111",
            # "@LuFerrari",
            # "@jhenycsel",
            # "@ValiaBeaut",
            # "@zarajoiner",
            # "@celinekiim",
            # "@AllieSchnacky",
            # "@theglobewanderers",
            # "@kailawenn",
            # "@ashlenjames",
            # "@renatocariani",
            # "@ImperioplayBR",
            # "@TheNicholasWalker",
            # "@dividendenpumper",
            # "@Munzfitness",
            # "@JasonArroza",
            # "@S-KAdventures",
            # "@Wothius",
            # "@Ilir09",
            # "@FutballMedia",
            # "@sarahfemina",
            # "@TwosomeTravellers",
            # "@AmyScarletona",
            # "@Paintyourlifestyle",
            # "@spain_walking_tour",
            # "@TravelholicTV",
            # "@prof.fergarcia",
            # "@INFOGASM-1",
            # "@shufosho",
            # "@nickhumph",
            # "@Theworldoffoods1",
            # "@sshouser31",
            # "@AlexBoultz",
            # "@SurfingWithNoz",
            # "@GoPro",
            # "@AndreaAdventures",
            # "@latestsightings",
            # "@savannaprivategamereserve",
            # "@WildlifeEncounter999",
            # "@songkick",
            # "@thetimmalcolm",
            # "@tomodell",
            # "@allrapnation",
            # "@SwiftAFNews",
            # "@WanderGoWalking",
            # "@bboydaydayfreakyday3893",
            # "@HiGoochieMama",
            # "@peopleareawesome",
            # "@premierleague",
            # "@Olympics",
            # "@wttglobal",
            # "@HeartbeatFilmsLouisiana",
            # "@stylemepretty",
            # "@Butt.erhand",
            # "@Cooking-ho5kl",
            # "@BiaArtDrawings",
            # "@AgushaLand",
            # "@Xendioshorts",
            # "@АльфаВозрождение",
            # "@Buildify1",
            #"@Equestrian-Edits",
            #"@MegaMachinesChannel",
            #"@ViaCarioca"
            #"@realmdbhtrap"
            #"@jockerfarmm"
            #"@truckmechanicfrompoland3720"
            #"@KnowledgeSnap7"
            #"@all-machines"
            #"@SimonFordman"
            #"@ZachChoi"
            #"@LukeMartin"
            #"@NaturalLifeTV2021"
            #"@Gara_Shorts",
            #"@galvsfood",
            #"@NickDiGiovanni",
            #"@Puma_Braige_official",
            #"@tyamonganimals",
            #"@un-cut-life",
            #"@cnnpop",
            #"@HenrySilvaDrum",
            #"@wianvandenberg",
            #"@elarshef1995",    
            #"@adissaputrapetualang3983",
            #"@Rikinho",
            #"@CoastalHuntSecrets",
            #"@MrDegreeOfficial",
            #"@Miss_Fresh",
            #"@Farmea",
            #"@sylcomlight",
            #"@MarinalvaEANatureza",
            #"@TheosToysCarsStories",
            #"@NJR-10n",
            #"@cookingwithalessandra",
            #"@SemMedo.",
            #"@prasantathefootballer",
            #"@kochiasmr",
            #"@experimentchannel12345",
            #"@Grau027",
            #"@Dhhdbd-m3b1g",
            #"@worldtrekdiaries",
            #"@soleenriaanvlogs",
            # "@VoiceMakers",
            # "@BRCartoonNetworkvideos",
            # "@NickelodeonEmPortugues",
            # "@7minutoz",
            # "@GeekCinema",
            # "@pixar",
            # "@disneyjr",
            # "@marvel",
            # "@dcofficial",
            # "@Animityworld",
            # "@LamenOtaku",
            # "@OtakuSafadão",
            # "@sitiodopicapaudesenho",
            # "@pocoyomusicainfantil",
            # "@catsfamilyemportuguesbrasil",
            "",
            # BRAIN ROT ACCOUNTS BELOW  : 
            # "@SHORT9999-s3t", 
            # "@warungtungtung", 
            # "@Kerstle", 
            # "@SamShortFunny9999",
            # "@B.hai20k",
            # "@sungkepgameshorts",
            # "@Ronalvagundes-r9",
            # "@JANNATIYT1",
            # "@tralalelooffice1",
            # "@TalezoraAi",
            # "@catlove-b4x",
            # "@IomnjYujo5",
            # "@sauravsingh-v7m",
            # "@Doodlevibes-34",
            # "@ZOOWAKE",
            # "@Funnyshortcreatorzz",
            # "@ANIMADOMUNDO1",
            # "@BigPencilMinecraft",
            # "@Williamhe-t4q",
            # "@JjkoWw",
            # "@LabibHome",
            # "@Jalifvfx",
            # "@BrainrotWorld_001",
            # "@joy_films_2.1",
            # "@PootisCraftYT",
            # "@dipakroy479",
            # "@alma3xd",
            # "@GoalPopz",
            # "@AwruGamer",
            # "@stevenz_25",
            # "@MelloTVai",
            # "@TheDregoEffect",
            # "@AIzanami",
            # "@CraftTune",
            # "@RihaShort",
            # "@NeedzersMod",
            # "@TinyPawChronicles",
            # "@mr.lupilupi",
            # "@natfamilyzz",
            # "@Titik_Hari",
            # "@GameRush2.0",
            # "@SCPUNKG",
            # "@faqih_busyiri",
            # "@SkyVibeAi",
            # "@Trend_Aii",
            # "@alma3xd",
            # "@AXTGAMING-s5y",
            # "@szcomics",
            # "@ScaryTeacherSQgame",
            # "@JalilRz-e7i",
            # "@Rountah",
            # "@hitato8677",
            # "@Rank1Studio",
            # "@BotTales-c7m",
            # "@AnimalCreation-j2r",
            # "@Pandakroo",
            # "@NeuraVibe333",
            # "@ronaldo_recall_1mm",
            # "@Faktologi12",
            # "@smile_som",
            # "@BrainPopFunny",
            # "@HeroinaJoaninha",
            # "@ManoneFails",
            # "@Mr.Catjoy",
            # "@PootisCraftYT",
            # "@blindayan",
            # "@GameVirus-h1s",
            # "@PintuSurga11",
            # "@Genzstories1219",
            # "@ToySparkleWorld",
            # "@starryskyanimation1120",
            # "@huhuqoqoo8069",
            # "@animemes-collection",
            # "@BrainrotSpaceOfficial",
            # "@Eleotan",
            # "@Pixel_tm_",
            # "@WeirdAnoma",
            # "@TheDregoEffec",
            # "@tung_tung_kentung",
            # "@quiznrot",
            # "@MythBoxAIVault",
            # "@chummbuckettt",
            # "@BrainrotMusicWorld",
            # "@aiasmrto",
            # "@Hopeorb",
            # "@brainrotplus0",
            # "@hasibsirrul573",
            # "@Brairotkingdom",
            # "@BrainrotGirlsK-Pop",
            # "@Brainrot_Girls_Dance",
            # "@italian-brainrot-l1h",
            # "@Hsratoon",
            # "@tung_tung_kentung",
            # "@SetimoHokage",
            # "@MsSparkTV",
            # "@MrPlonkTV",
            # "@TinyTotsTV-v3e",
            # "@BGSoothingS",
            # "@Palbenek",
            # "@ItalianBrainrot-f3q",
            # "@footytransformation",
            # "@OddMythUS",
            # "@LoopLenz",
            # "@pawonanimal",
            # "@Tonngs-d3r",
            # "@FuFui-k7y",
            # "@Animai08",
            # "@FunAILab-g5n",
            # "@TimeLoops-n2e",
            # "@warungtungtung",
            # "@Jovita_Stories",
            # "@ZiYummy_ai",
            # "@Animallife-z2b",
            #"@WizzyVibesOfficial",
            # "@PixelBunny-g7t",
            # "@patrulhaaniverso",
            # "@ALOMANILINI",
        ]
    run_batch(usernames, "y", save_imgs=True)
