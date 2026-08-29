#!/usr/bin/env python3
# HALO & GRAIN static site generator (V1)
import json, os, html, re

SITE = "/home/claude/site"
IMG = json.load(open("/home/claude/images_map.json"))

# ---------------- CONFIG ----------------
BRAND      = "Halo & Grain"
DOMAIN     = "https://example.com"        # <-- replace at launch
PHONE_DISP = "+91 98765 43210"
PHONE_TEL  = "+919876543210"
WA         = "919876543210"
EMAIL      = "hello@haloandgrain.example"
ADDRESS    = "No. 21, 2nd Avenue, Besant Nagar, Chennai, Tamil Nadu 600090"
CITY       = "Chennai"
YEAR       = "2026"

# ---------------- CATEGORIES ----------------
CATS = {
 "weddings":  {"label":"Weddings & Couples"},
 "maternity": {"label":"Maternity"},
 "baby":      {"label":"Baby & Newborn"},
 "ceremonies":{"label":"Ceremonies & Functions"},
 "portraits": {"label":"Portraits & Fashion"},
 "commercial":{"label":"Commercial & Product"},
 "video":     {"label":"Film & Video"},
 "events":    {"label":"Events & Celebrations"},
 "print":     {"label":"Albums, Frames & Prints"},
 "studio":    {"label":"Studio & Near You"},
}

INCLUDES = {
 "weddings":[("Full-day coverage","From the morning rituals to the last song, nothing missed."),
   ("Two shooters + assistant","Wide moments and tight reactions captured at the same time."),
   ("Candid + traditional","Honest, unposed frames alongside the portraits families expect."),
   ("Cinematic highlight film","A 3–4 minute film, scored and colour-graded."),
   ("Album + online gallery","A premium album plus a private gallery to share.")],
 "maternity":[("Studio or outdoor","A calm, unhurried session at your own pace."),
   ("Wardrobe & prop guidance","Flowy gowns, drapes and simple styling advice."),
   ("Soft natural-light look","Gentle, flattering light and skin-kind retouching."),
   ("Partner & sibling frames","Room for the whole family in the story."),
   ("Print-ready gallery","High-resolution images delivered in 2–3 weeks.")],
 "baby":[("Baby-led pacing","We shoot around naps, feeds and moods, never the clock."),
   ("Safe, hygienic setups","Clean props, sanitised sets and gentle handling."),
   ("Timeless styling","Neutral tones that won't date the photographs."),
   ("Parents in the frame","Because the first weeks are yours too."),
   ("Soft retouch + gallery","Delicate edits and a shareable online gallery.")],
 "ceremonies":[("Complete ritual coverage","Every rite and blessing documented in order."),
   ("Discreet during the rites","Present for the moments, invisible during them."),
   ("Family group portraits","Organised quickly so guests aren't kept waiting."),
   ("Fast sneak peeks","A first set within 72 hours to share with family."),
   ("Prints & album on request","Frames and albums to keep the day at home.")],
 "portraits":[("Pre-shoot direction","A quick plan on looks, outfits and locations."),
   ("Studio or on-location","Controlled light or a real-world backdrop."),
   ("Multiple looks","Room for outfit and mood changes in one session."),
   ("Editorial retouching","Clean, natural finishing that still looks like you."),
   ("High-res + print options","Web files for sharing, prints for keeping.")],
 "commercial":[("Brief & shot-list first","We plan every frame against your goals."),
   ("Consistent light & colour","A repeatable look across your whole catalogue."),
   ("Fast turnaround","Edited, format-ready files on a tight timeline."),
   ("Usage-ready exports","Sized for web, marketplace and print."),
   ("Volume-friendly pricing","Better rates as the shot count grows.")],
 "video":[("Multi-cam coverage","Nothing missed, cut from several angles."),
   ("Story & sound first","Scripting, interviews, music and clean audio."),
   ("Colour grade + mix","A finished look and balanced sound design."),
   ("Social cut-downs","Verticals and teasers sized for every platform."),
   ("Delivered in 2–4 weeks","Drafts for review, then the final masters.")],
 "events":[("Multi-hour coverage","We stay for the whole event, start to finish."),
   ("Candid + stage","Reactions in the crowd and clean stage frames."),
   ("Same-day highlights","An optional quick set before guests leave."),
   ("Discreet team","Professional, low-profile, dressed for the room."),
   ("Quick full gallery","Every keeper delivered within days.")],
 "print":[("Premium materials","Archival papers, real wood and quality boards."),
   ("Colour-calibrated proofs","What you approve is what you receive."),
   ("Custom sizes & layouts","Designed to fit your photos, not a preset."),
   ("Doorstep delivery","Carefully packed and shipped across India."),
   ("Bulk & trade pricing","Sensible rates for volume and repeat orders.")],
 "studio":[("Walk-in friendly","Quick sessions without a big production."),
   ("Passport to portraits","Everyday needs and proper portraits alike."),
   ("Instant prints","Printed on the spot when you need them fast."),
   ("Local, experienced team","People who've shot every kind of occasion."),
   ("Honest, upfront pricing","Clear packages, with no surprises.")],
}

# ---------------- SERVICES (order = user's list) ----------------
# slug : (Display Name, category, hero-subline, para1, para2)
S = {
"wedding-photographers":("Wedding Photographers","weddings",
 "Editorial wedding photography and cinematic films across Chennai, Tamil Nadu and beyond.",
 "A wedding is a long, loud, emotional day — and the best photographs of it are usually the ones nobody posed for. We cover the whole arc, from the quiet getting-ready hours to the last dance, shooting candidly and staying out of the way of your actual day.",
 "You get both worlds: honest, in-the-moment frames and the classic family portraits everyone will ask for. Every wedding is shot by at least two photographers, backed up in triplicate, and delivered as a gallery and film you'll still open in twenty years."),
"pre-wedding-photoshoot":("Pre Wedding Photoshoot","weddings",
 "Relaxed pre-wedding shoots on location — the story before the story.",
 "A pre-wedding shoot is the one time before the wedding when it's just the two of you and a camera. We use it to get you comfortable, find your natural chemistry, and make images that feel like you rather than a set of props.",
 "We'll help pick locations and looks — a beach at dawn, a heritage street, a resort — and shoot at the light that flatters most. It doubles as great practice for the wedding day and gives you images for invites and save-the-dates."),
"maternity-and-pregnancy-photographers":("Maternity & Pregnancy Photographers","maternity",
 "Soft, celebratory maternity portraits, in studio or outdoors.",
 "The weeks before a baby arrives are worth keeping. Our maternity sessions are calm and unhurried, built around flattering natural light and gentle direction so you feel at ease, not on display.",
 "We guide you on gowns, drapes and simple styling, and leave room for your partner and older children in the frame. The best window is usually 28–34 weeks — reach out early and we'll plan the timing with you."),
"baby-shower-photographers":("Baby Shower Photographers","baby",
 "Warm, candid coverage of the baby shower and every guest who came.",
 "A baby shower is equal parts celebration and reunion. We cover the décor and the details, the games and the gifts, and — most importantly — the candid reactions and the family who turned up to bless the mum-to-be.",
 "We stay unobtrusive so the day feels like a party, not a shoot, and organise quick group portraits so nobody's kept waiting. Sneak peeks reach you within a couple of days to share with everyone who couldn't make it."),
"events-photographers":("Events Photographers","events",
 "Discreet, reliable coverage for functions, launches and celebrations.",
 "Whether it's a milestone celebration, a cultural function or a company event, good event coverage is invisible while it's happening and complete when it's done. We plan around your run-of-show so the key moments are never missed.",
 "Our team blends into the room, covers both the stage and the crowd, and turns work around fast — with an optional same-day highlight set for events where you want photos before guests head home."),
"portfolio-shoot":("Portfolio Shoot","portraits",
 "Portfolio sessions for models, actors and creatives who need range.",
 "A strong portfolio shows range in a handful of frames. We plan looks, moods and lighting setups with you beforehand, then shoot efficiently so you leave with a set that works for castings, agencies and social.",
 "Studio or location, multiple outfits, and honest editorial retouching that still looks like you. We'll help you sequence and select the final images, not just hand over a folder of files."),
"product-e-commerce-photographers":("Product & E-Commerce Photographers","commercial",
 "Clean, consistent product photography built for online selling.",
 "Product photos do one job: make someone confident enough to buy. We shoot on white, on lifestyle sets and in detail — with lighting and colour kept consistent across your whole catalogue so your store looks like one brand.",
 "Files come sized and formatted for your marketplace, website and ads, on a turnaround that keeps up with your launches. And the more you shoot, the better the per-image rate."),
"birthday-photographers":("Birthday Photographers","events",
 "Bright, joyful birthday coverage for kids and grown-ups alike.",
 "Birthdays move fast and don't do second takes. We keep pace with the cake, the games and the chaos, catching the real reactions rather than lining people up for stiff group shots.",
 "From a first-birthday theme setup to a milestone party, we cover the décor, the candids and the family portraits, and deliver a gallery quickly while the memory's still fresh."),
"newborn-photography":("Newborn Photography","baby",
 "Gentle newborn portraits, shot safely and at your baby's pace.",
 "Newborn sessions run on the baby's clock, not ours. We work slowly and safely around naps and feeds, with clean props and simple, timeless styling that won't look dated in a decade.",
 "The first two weeks are the ideal window for those curled-up sleepy frames, so book ahead of your due date. Parents and siblings are always welcome in the photos — these first days belong to all of you."),
"engagement-photographers":("Engagement Photographers","weddings",
 "Coverage for the ring ceremony and the celebration around it.",
 "The engagement is where two families meet and the celebration begins. We cover the ring exchange, the rituals and the mingling, balancing the formal moments with the candid warmth in the room.",
 "Expect quick, organised family portraits and a set of couple frames you can use for the wedding invites — delivered fast so the momentum carries straight into the planning."),
"family-shoot":("Family Shoot","portraits",
 "Relaxed family portraits that actually look like your family.",
 "The best family photos aren't the stiff, everyone-say-cheese kind — they're the ones with real laughter and a bit of mess. We keep sessions playful, especially with young kids, so the images feel like your family on a good day.",
 "Studio or a favourite outdoor spot, one outfit or several, grandparents included. You'll get a mix of together frames and individual portraits, finished naturally and ready to print."),
"house-warming-ceremony-photographers":("House Warming Ceremony Photographers","ceremonies",
 "Coverage for the Gruhapravesam and the celebration that follows.",
 "A housewarming marks a real milestone, and the rituals deserve to be documented properly. We cover the pooja and the traditions in order, plus the first meal and the family gathering in the new home.",
 "We're discreet during the rites and quick with the group portraits, so the day stays about family rather than the camera. Prints and a small album are easy to add if you'd like to keep the day on a wall."),
"photo-restoration-service":("Photo Restoration Service","print",
 "Careful digital restoration of damaged and faded photographs.",
 "Old photographs fade, tear, crease and stain — but most can be brought back. We digitally repair damage, rebuild missing areas, correct colour and sharpen detail, treating each image by hand rather than with a one-click filter.",
 "Torn wedding portraits, water-damaged prints, faded ancestor photos — send us a scan or the original and we'll show you what's recoverable. Restored files can be re-printed and framed to keep for the next generation."),
"post-wedding-photoshoot":("Post Wedding Photoshoot","weddings",
 "A relaxed shoot after the wedding, without the day's rush.",
 "The wedding day is a blur; a post-wedding shoot is the calm after it. In your finery but with none of the schedule, we get the unhurried couple portraits there was never time for on the day itself.",
 "Shoot at a location that means something to you, or somewhere purely beautiful — a resort, a backwater, a heritage site. It's the easiest way to get frame-worthy images without the wedding-day pressure."),
"naming-ceremony-photography":("Naming Ceremony Photography","ceremonies",
 "Coverage for the naming ceremony and the family's first blessings.",
 "A naming ceremony is a baby's formal welcome into the family, and it happens only once. We document the rituals, the whispered name and the elders' blessings gently, keeping our distance from the baby and the rites.",
 "Alongside the traditions we capture the candid warmth — cousins meeting the newborn, grandparents holding them — and organise family portraits quickly so the baby isn't overtired."),
"upanayana-photography":("Upanayana Photography","ceremonies",
 "Respectful coverage of the sacred thread ceremony.",
 "The Upanayanam is a solemn, meaningful rite of passage. We document each stage of the ceremony faithfully and discreetly — the homa, the mantras, the sacred thread — without ever intruding on the proceedings.",
 "We balance the ritual coverage with the family celebration around it, and deliver organised group portraits of the many relatives who gather for it. Albums and prints are available to preserve the occasion properly."),
"shastipurthi-photography":("Shastipurthi Photography","ceremonies",
 "Coverage for the 60th-year Shashtiabdapoorthi celebration.",
 "A Shashtipurthi honours sixty years of life and marriage, and it brings the generations together. We cover the ceremony and the renewal of vows with the dignity it deserves, and the joyful reunion that surrounds it.",
 "This is a rare gathering of the whole extended family, so we make family portraits a priority — organised, unhurried and complete. A commemorative album is the natural way to keep a day like this."),
"photo-frames":("Photo Frames","print",
 "Quality custom frames for your favourite photographs.",
 "A photograph earns its place on a wall in the right frame. We offer a range of materials, sizes and finishes — classic wood, clean modern profiles, collage layouts — matched to the image and the room it'll live in.",
 "Send us the photos and we'll advise on sizing, mounting and finish, print on archival stock, and deliver framed and ready to hang. Bulk orders for weddings and gifting are welcome."),
"album-designers-and-printers":("Album Designers & Printers","print",
 "Bespoke album design and premium printing.",
 "An album is how a wedding or event survives off a phone screen. We design each spread by hand around your story — pacing, sequencing and layout — rather than dropping images into a template.",
 "Printed on premium stock with quality binding and a protective finish, built to be handled and passed around for decades. We handle design, proofing and printing end to end, including reprints for family."),
"candid-wedding-photography":("Candid Wedding Photography","weddings",
 "Unposed, in-the-moment wedding storytelling.",
 "Candid photography is about catching the moment before it's gone — the tear during the vows, the uncle mid-laugh, the quiet glance between the couple. We shoot documentary-style, reading the room rather than directing it.",
 "It pairs naturally with traditional coverage, so you get the honest frames and the classic portraits both. Two shooters mean the candid and the formal are covered at once, never one at the cost of the other."),
"candid-videographers":("Candid Videographers","video",
 "Documentary-style wedding and event films.",
 "Candid videography treats your day like a film, not a recording. We follow the story as it unfolds, catching real audio and real reactions, then cut it into something with rhythm and emotion rather than a chronological log.",
 "The result is a highlight film you'll actually rewatch, plus longer edits of the key ceremonies. We work quietly alongside the photo team so neither gets in the other's frame."),
"professional-videography":("Professional Videography","video",
 "Polished video production for weddings, brands and events.",
 "Good video is more than pointing a camera — it's coverage, sound, lighting and edit working together. We bring multi-camera setups, clean audio and a considered edit to weddings, corporate work and events alike.",
 "From a wedding highlight film to a brand video or event aftermovie, we plan the shoot around the story you want told, then colour-grade and mix the final cut to a professional standard."),
"corporate-photographers":("Corporate Photographers","commercial",
 "Professional headshots, teams, offices and corporate events.",
 "Corporate photography is your brand's first impression — on your website, your profiles and in the press. We deliver consistent headshots, natural team and workplace images, and clean coverage of conferences and events.",
 "We work fast and unobtrusively around your schedule, keep the look consistent across your whole team, and deliver retouched, format-ready files on deadline. On-site or in studio, one person or a whole floor."),
"christian-wedding-photographers":("Christian Wedding Photographers","weddings",
 "Coverage attuned to the church ceremony and the reception.",
 "A Christian wedding has its own rhythm — the processional, the vows, the exchange of rings, the reception that follows. We know where to be for each, and how to shoot respectfully within a church without disrupting the service.",
 "We balance the reverent moments with the candid joy of the celebration, and cover both with two photographers so nothing overlaps. The result is a gallery and film true to the day's grace and its happiness."),
"muslim-wedding-photographers":("Muslim Wedding Photographers","weddings",
 "Sensitive coverage of the Nikah and the walima.",
 "A Muslim wedding spans the Nikah, the walima and the family gatherings around them, each with its own meaning. We cover them attentively and respectfully, mindful of customs and comfort throughout.",
 "We can arrange the coverage your family prefers, stay discreet during the ceremony, and focus on the candid warmth and the portraits both families will treasure. Coverage, album and film are all available."),
"digital-photo-studio-near-me":("Digital Photo Studio Near Me","studio",
 "A full-service digital photo studio for everyday needs.",
 "Sometimes you just need a proper studio nearby — for a passport photo, a portrait, an instant print or a quick family sitting. Our digital studio handles all of it with professional lighting and same-day output.",
 "Walk in for the small things or book ahead for a full session. Prints on the spot, files by email, and an experienced team who'll make sure you leave with something you're happy to use."),
"puberty-function-photographers":("Puberty Function Photographers","ceremonies",
 "Coverage for the coming-of-age Ritu Kala Samskara.",
 "The puberty function is a proud family celebration, and it deserves coverage that's both traditional and tasteful. We document the rituals, the blessings and the grand family gathering with care and discretion.",
 "We handle the many relatives and the group portraits smoothly, catch the candid joy around the ceremony, and deliver a gallery — and album, if you'd like — that does the occasion justice."),
"portrait-photography":("Portrait Photography","portraits",
 "Considered portraits for individuals, professionals and creatives.",
 "A good portrait says something true about the person in it. We shoot with intention — light, expression and direction working together — whether it's a professional headshot, a personal portrait or a creative concept.",
 "Studio or location, a single strong look or several, finished with natural retouching. We'll direct you through it, so even if you 'hate having your photo taken', you'll walk away with images you actually like."),
"karizma-album-printing":("Karizma Album Printing","print",
 "Premium Karizma-style albums, designed and printed.",
 "Karizma albums set the standard for wedding books — flush-mount pages, seamless spreads and a substantial, luxurious feel. We design each spread around your story and print to that premium standard.",
 "Thick, rigid pages that lie flat, rich colour and durable binding built to be handled for decades. We manage design, proofing and printing together, with reprints available for parents and family."),
"drone-photography":("Drone Photography","commercial",
 "Aerial photography and video for weddings, events and property.",
 "A drone changes the scale of a story — the sweep of a wedding venue, the crowd at an event, a property from above. We add licensed aerial coverage that grounds your film and photos in a sense of place.",
 "Cinematic aerial video and stills, flown safely and legally, integrated with your ground coverage rather than bolted on. Ideal for destination weddings, large functions, resorts and real estate."),
"baby-photoshoot":("Baby Photoshoot","baby",
 "Playful baby portraits from newborn to first birthday.",
 "Babies change month to month, and a shoot catches a stage you'll otherwise forget. We keep sessions gentle and led by the baby, with simple setups and lots of patience for the smiles that come on their own schedule.",
 "Milestone shoots, sitter sessions, cake-smash first birthdays — we tailor the setup to the age and mood. Parents in the frame, safe props, and a soft, timeless finish."),
"photographers-near-me":("Photographers Near Me","studio",
 "Experienced local photographers, ready when you are.",
 "When you search for a photographer nearby, you want someone reachable, reliable and good — not a stock listing. We're a local team covering Chennai and across Tamil Nadu for every kind of occasion.",
 "Weddings, events, portraits, products, functions — one team, consistent quality, honest pricing. Message us with what you need and we'll come back quickly with availability and a clear quote."),
"cradle-ceremony":("Cradle Ceremony","ceremonies",
 "Coverage for the cradle ceremony and the baby's first days.",
 "The cradle ceremony places the baby in the family cradle for the first time — a tender, brief moment surrounded by relatives. We document it gently, keeping our distance from the newborn while catching the ritual and the reactions.",
 "Around the ceremony we cover the décor, the candid family warmth and the group portraits everyone will want. Sneak peeks land within days so you can share the news with those who couldn't attend."),
"photographers":("Photographers","studio",
 "A full-service photography and film studio in Chennai.",
 "Halo & Grain is a photography and videography studio covering the whole range — weddings, portraits, events, commercial work, functions and film. Whatever the occasion, it's handled by the same small, experienced team.",
 "That means consistent quality, one point of contact and honest pricing across everything we do. Tell us what you're planning and we'll point you to the right coverage and a clear quote."),
"video-editing-services":("Video Editing Services","video",
 "Professional editing for wedding, event and brand footage.",
 "Great footage still needs a great edit. We take your raw video — or ours — and turn it into a finished film: paced, colour-graded, sound-mixed and cut for the platform it's headed to.",
 "Wedding highlight films, event aftermovies, brand and social content, reels and teasers. Send us the material and a reference for the feel you're after, and we'll shape it into something worth watching."),
"corporate-video-production":("Corporate Video Production","video",
 "End-to-end video production for brands and businesses.",
 "A corporate video should make your business look like itself, at its best. We handle production end to end — scripting, shoot, interviews, b-roll and edit — for brand films, product videos, testimonials and internal content.",
 "Multi-camera coverage, clean audio, professional lighting and a considered edit, delivered in the formats your channels need. We plan every video around a clear goal, not just a nice-looking cut."),
"personalized-coffee-mug-printing-service":("Personalized Coffee Mug Printing Service","print",
 "Custom printed mugs for gifts, events and brands.",
 "A printed mug is a small, daily reminder of a photo, a moment or a brand. We print your images, messages and logos onto quality mugs with durable, dishwasher-safe results.",
 "Perfect for wedding favours, birthdays, corporate gifting and personal keepsakes. Single mugs or bulk orders, designed with you and delivered to your door across India."),
"freelance-photographers":("Freelance Photographers","studio",
 "Flexible freelance photography for any brief or budget.",
 "Not every shoot needs a big production. As a flexible freelance team, we scale to the brief — a single photographer for an intimate event, or a full crew for a wedding — without the overheads of a large studio.",
 "That flexibility keeps pricing honest and communication direct: you deal with the person actually shooting your event. Tell us the brief and the budget and we'll shape coverage to fit."),
"canvera-album-design-and-printing":("Canvera Album Design & Printing","print",
 "Canvera-style album design and quality printing.",
 "Canvera albums are a trusted choice for wedding and event books — well-made, richly printed and built to last. We design each album around your images and print to that dependable standard.",
 "Hand-designed spreads, quality paper and binding, and careful proofing before anything goes to print. We manage the whole process and handle reprints for family who'll inevitably want their own copy."),
"elements-resort-prewedding-shoot":("Elements Resort Prewedding Shoot","weddings",
 "Pre-wedding shoots at Elements Resort and venues like it.",
 "A resort pre-wedding shoot gives you variety in one place — landscaped grounds, water, architecture and privacy — without hopping between locations. Elements and venues like it are made for exactly this.",
 "We plan the looks and timing around the resort's best light and spots, and handle the shoot start to finish. You get a relaxed day, a change of scenes, and couple portraits that feel like a getaway."),
"baby-photoshoot-places":("Baby Photoshoot Places","baby",
 "The best spots and setups for a baby photoshoot.",
 "Where you shoot shapes how a baby photoshoot feels. We work in a calm home setting, in our studio with clean props, or at gentle outdoor spots — matched to your baby's comfort and the look you want.",
 "Not sure where to start? Tell us the age and the vibe you're after, and we'll suggest the setting and setup that'll work best, then handle everything on the day so you can just enjoy it."),
"maternity-photoshoot-places":("Maternity Photoshoot Places","maternity",
 "Beautiful locations and studio setups for maternity portraits.",
 "The right location makes a maternity shoot. We shoot in a soft-lit studio, at the beach or backwaters, in green outdoor settings, or at home — chosen to flatter and to feel like you.",
 "We'll recommend spots based on your due date, the season and the mood you want, and plan the timing around the best light. Comfort comes first, always — these sessions are meant to feel easy."),
"anniversary-photoshoot":("Anniversary Photoshoot","weddings",
 "Celebrate the years with a relaxed anniversary shoot.",
 "An anniversary shoot is a lovely way to mark the years — whether it's your first or your fiftieth. We keep it relaxed and personal, catching the ease that comes from knowing each other well.",
 "Recreate an old photo, return to a place that matters, or simply dress up and enjoy an evening in front of the camera. Bring the family for a milestone year, or keep it just the two of you."),
"holy-communion-baptism-photoshoot":("Holy Communion & Baptism Photoshoot","ceremonies",
 "Coverage for baptisms, first communion and confirmations.",
 "A baptism or first communion is a meaningful step in a child's faith and a proud family day. We cover the church ceremony respectfully and the celebration that follows with warmth.",
 "We're mindful of the service and discreet during it, then organised for the family portraits afterwards. Prints and a small album are easy to add to keep the occasion beyond the day."),
"indoor-maternity-photoshoot":("Indoor Maternity Photoshoot","maternity",
 "Elegant indoor and studio maternity sessions.",
 "An indoor maternity shoot gives you full control — of light, of privacy, of comfort. In our studio we shape soft, flattering light around you, with drapes, gowns and simple sets that keep the focus where it belongs.",
 "Ideal in the heat, the rain, or simply when you'd rather be somewhere calm and private. We guide the posing gently and keep the whole session unhurried and easy."),
"fashion-photographers":("Fashion Photographers","portraits",
 "Editorial and fashion photography with a point of view.",
 "Fashion photography is where styling, light and attitude meet. We shoot editorial and lookbook work with a strong point of view — for designers, boutiques, models and brands who want more than a plain catalogue.",
 "We collaborate on concept, styling and location, direct the shoot with intent, and finish with retouching that respects the clothes and the skin. Studio or location, single looks or a full editorial story."),
"babys-backyard-studio":("Baby's Backyard Studio","baby",
 "Natural-light baby sessions in a relaxed backyard studio.",
 "A backyard studio blends the comfort of home with the polish of a set — soft natural light, greenery, and a calm, unhurried space where babies tend to relax and parents do too.",
 "It's an easy, gentle setting for newborn, milestone and sitter sessions, with none of the formality of a hard studio. We keep props simple and the pace led entirely by your little one."),
}

ORDER = list(S.keys())  # preserves insertion = user's list order

# ---------------- IMAGE DATA (baked fallback + OG paths) ----------------
# Read the current file listing once, to (a) bake a same-origin fallback and
# (b) compute OG image URLs. At runtime the site reads manifest.json instead,
# so add/rename/delete in images/<slug>/ is picked up dynamically.
_raw = open("/home/claude/pd/assets/gallery-data.js", encoding="utf-8").read()
GALLERY = json.loads(_raw[_raw.index("{"): _raw.rindex("}") + 1])
FILES = {c["slug"]: list(c.get("files", [])) for c in GALLERY.get("categories", [])}

def og_for(slug):
    fs = FILES.get(slug) or []
    return f"{DOMAIN}/images/{slug}/{fs[0]}" if fs else f"{DOMAIN}/images/cover.jpg"

# ---------------- PARTIALS ----------------
def esc(t): return html.escape(t, quote=True)

def head(title, desc, canon, prefix, og_img, extra_ld=""):
    ld_local = json.dumps({
      "@context":"https://schema.org","@type":"LocalBusiness","name":BRAND,
      "url":DOMAIN+"/","telephone":PHONE_TEL,"priceRange":"₹₹₹","image":og_img,
      "address":{"@type":"PostalAddress","streetAddress":"No. 21, 2nd Avenue, Besant Nagar",
        "addressLocality":"Chennai","addressRegion":"TN","postalCode":"600090","addressCountry":"IN"},
      "geo":{"@type":"GeoCoordinates","latitude":13.0002,"longitude":80.2668},
      "openingHours":"Mo-Sa 10:00-19:00",
      "areaServed":["Chennai","Pondicherry","Bengaluru","Tamil Nadu"],
      "sameAs":["https://www.instagram.com/"]
    }, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#14110E">
<link rel="stylesheet" href="{prefix}assets/css/main.css">
<script>(function(){{try{{var p=new URLSearchParams(location.search);if(p.get('c'))document.documentElement.classList.add('pre-brand');setTimeout(function(){{document.documentElement.classList.remove('pre-brand');}},1500);}}catch(e){{}}}})();</script>
<script src="{prefix}assets/js/branding.js" defer></script>
<script type="application/ld+json">{ld_local}</script>
{extra_ld}
</head>
<body data-root="{prefix}">
<a class="skip" href="#main">Skip to content</a>
"""

def mega_menu(prefix, active_slug=""):
    cols = []
    for ckey, cmeta in CATS.items():
        members = [s for s in ORDER if S[s][1] == ckey]
        if not members:
            continue
        lis = "\n".join(
            f'''            <li><a href="{prefix}services/{s}.html"{" aria-current=\"page\"" if s==active_slug else ""}>{esc(S[s][0])}</a></li>'''
            for s in members)
        cols.append(f'''          <div class="mega-col">
            <span class="mega-cat">{esc(cmeta["label"])}</span>
            <ul>
{lis}
            </ul>
          </div>''')
    grid = "\n".join(cols)
    return f'''      <li class="has-mega">
        <button class="mega-btn" id="megaBtn" aria-haspopup="true" aria-expanded="false" aria-controls="megaPanel">Services <span class="caret" aria-hidden="true">&#9662;</span></button>
        <div class="mega" id="megaPanel">
          <div class="mega-inner">
            <div class="mega-head">
              <span class="exif no-rule">All services &middot; {len(ORDER)}</span>
              <a href="{prefix}services.html">Services overview &rarr;</a>
            </div>
            <div class="mega-grid">
{grid}
            </div>
          </div>
        </div>
      </li>'''

def nav(prefix, solid=False, active="", active_slug=""):
    cls = "nav solid" if solid else "nav"
    return f"""<header class="{cls}" id="nav">
  <a class="brand" href="{prefix}index.html" data-b="name">Halo <span>&amp;</span> Grain</a>
  <nav aria-label="Primary">
    <ul class="nav-links" id="navLinks">
      <li><a href="{prefix}index.html#work">Work</a></li>
      <li><a href="{prefix}index.html#reel">Films</a></li>
{mega_menu(prefix, active_slug)}
      <li><a href="{prefix}index.html#about">Studio</a></li>
      <li><a href="{prefix}index.html#pricing">Pricing</a></li>
      <li><a href="{prefix}index.html#contact">Contact</a></li>
    </ul>
  </nav>
  <div class="nav-cta">
    <a class="btn btn--ghost" href="{prefix}services.html">All services</a>
    <a class="btn btn--gold" href="{prefix}index.html#contact">Book a date</a>
    <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks" aria-label="Open menu"><span></span></button>
  </div>
</header>
"""

# top service links for footer
FOOoter_LINKS = ["wedding-photographers","pre-wedding-photoshoot","newborn-photography",
  "events-photographers","product-e-commerce-photographers","professional-videography"]

def footer(prefix):
    svc = "\n".join(
      f'          <li><a href="{prefix}services/{s}.html">{esc(S[s][0])}</a></li>'
      for s in FOOoter_LINKS)
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="brand-col">
        <span class="brand" data-b="name">Halo <span>&amp;</span> Grain</span>
        <p class="about-line">Wedding &amp; film studio in {CITY}. Warm light, honest photographs, and films you'll still watch in twenty years.</p>
        <div class="socials">
          <a href="https://www.instagram.com/" data-href="instagram" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2c2.7 0 3 0 4.1.1 1 0 1.7.2 2.3.5.6.2 1.1.5 1.6 1s.8 1 1 1.6c.3.6.4 1.3.5 2.3.1 1.1.1 1.4.1 4.1s0 3-.1 4.1c0 1-.2 1.7-.5 2.3a4.4 4.4 0 0 1-1 1.6 4.4 4.4 0 0 1-1.6 1c-.6.3-1.3.4-2.3.5-1.1.1-1.4.1-4.1.1s-3 0-4.1-.1c-1 0-1.7-.2-2.3-.5a4.4 4.4 0 0 1-1.6-1 4.4 4.4 0 0 1-1-1.6c-.3-.6-.4-1.3-.5-2.3C2 15 2 14.7 2 12s0-3 .1-4.1c0-1 .2-1.7.5-2.3a4.4 4.4 0 0 1 1-1.6 4.4 4.4 0 0 1 1.6-1c.6-.3 1.3-.4 2.3-.5C9 2 9.3 2 12 2zm0 5a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.8 7a1.2 1.2 0 1 1-2.4 0 1.2 1.2 0 0 1 2.4 0z"/></svg></a>
          <a href="https://www.youtube.com/" data-href="youtube" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23 12s0-3.2-.4-4.7a2.5 2.5 0 0 0-1.7-1.7C19.4 5.2 12 5.2 12 5.2s-7.4 0-8.9.4a2.5 2.5 0 0 0-1.7 1.7C1 8.8 1 12 1 12s0 3.2.4 4.7a2.5 2.5 0 0 0 1.7 1.7c1.5.4 8.9.4 8.9.4s7.4 0 8.9-.4a2.5 2.5 0 0 0 1.7-1.7C23 15.2 23 12 23 12zM9.8 15.3V8.7l5.7 3.3-5.7 3.3z"/></svg></a>
        </div>
      </div>
      <div>
        <h4>Popular services</h4>
        <ul>
{svc}
          <li><a href="{prefix}services.html">View all 47 →</a></li>
        </ul>
      </div>
      <div>
        <h4>We shoot in</h4>
        <ul>
          <li><a href="{prefix}index.html#contact">Chennai</a></li>
          <li><a href="{prefix}index.html#contact">Pondicherry</a></li>
          <li><a href="{prefix}index.html#contact">Bengaluru</a></li>
          <li><a href="{prefix}index.html#contact">Coimbatore</a></li>
          <li><a href="{prefix}index.html#contact">Destination</a></li>
        </ul>
      </div>
      <div>
        <h4>Get in touch</h4>
        <ul>
          <li><a href="tel:{PHONE_TEL}" data-href="tel" data-b="phone">{PHONE_DISP}</a></li>
          <li><a href="mailto:{EMAIL}" data-href="mail" data-b="email">{EMAIL}</a></li>
          <li><a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp us</a></li>
          <li><a href="{prefix}privacy.html">Privacy</a></li>
          <li><a href="{prefix}terms.html">Terms</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {YEAR} {esc(BRAND)} Studio · {CITY}</span>
      <span data-b="address">{ADDRESS}</span>
    </div>
  </div>
</footer>
"""

def wa_float(prefix, msg="Hi Halo & Grain, I'd like to check your availability."):
    from urllib.parse import quote
    return f"""<a class="wa-float" id="waFloat" href="https://wa.me/{WA}?text={quote(msg)}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M.5 23.5l1.6-5.9a11.4 11.4 0 1 1 4.3 4.3L.5 23.5zM6.7 20l.4.2a9.5 9.5 0 1 0-3.3-3.3l.2.4-1 3.6 3.7-.9zM17.4 14.3c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1-.2.2-.6.8-.8 1-.1.1-.3.2-.5 0-.2-.1-1-.4-1.9-1.1-.7-.6-1.2-1.4-1.3-1.6-.1-.2 0-.4.1-.5l.4-.4c.1-.2.2-.3.2-.5s0-.3 0-.4c-.1-.1-.5-1.3-.7-1.7-.2-.5-.4-.4-.5-.4h-.5c-.1 0-.4.1-.6.3-.2.2-.8.8-.8 1.9s.8 2.2.9 2.4c.1.2 1.6 2.5 3.9 3.5 1.6.7 2 .6 2.4.5.5-.1 1.4-.6 1.6-1.1.2-.5.2-1 .1-1.1 0-.1-.2-.1-.4-.2z"/></svg>
</a>
<script src="{prefix}assets/js/images-data.js" defer></script>
<script src="{prefix}assets/js/gallery.js" defer></script>
<script src="{prefix}assets/js/main.js" defer></script>
</body>
</html>"""

# ---------------- SERVICE PAGE ----------------
def service_page(slug):
    name, cat, sub, p1, p2 = S[slug]
    catlabel = CATS[cat]["label"]
    canon = f"{DOMAIN}/services/{slug}.html"
    title = f"{name} in {CITY} | {BRAND}"
    desc  = f"{name} in {CITY} — {sub} Photography & film by {BRAND}, covering {CITY} & across Tamil Nadu."
    desc  = desc[:158]
    from urllib.parse import quote
    wamsg = f"Hi Halo & Grain, I'd like to enquire about {name}."

    # includes
    inc = "\n".join(
      f'''        <div class="include"><span class="n">{i+1:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'''
      for i,(t,d) in enumerate(INCLUDES[cat]))

    # gallery is rendered at runtime from manifest.json (see gallery.js)
    # related (same category, up to 4) — thumbnails filled dynamically too
    rel = [s for s in ORDER if S[s][1]==cat and s!=slug][:4]
    rel_html = "\n".join(
      f'''        <a class="related" href="{r}.html" data-img="{r}" data-i="0"><span>{esc(S[r][0])}</span></a>'''
      for r in rel) or '<p>More services coming soon.</p>'

    # schema: Service + Breadcrumb
    ld = json.dumps({"@context":"https://schema.org","@type":"Service","serviceType":name,
      "provider":{"@type":"LocalBusiness","name":BRAND,"telephone":PHONE_TEL},
      "areaServed":["Chennai","Pondicherry","Bengaluru","Tamil Nadu"],
      "url":canon,"description":sub}, ensure_ascii=False)
    bc = json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},
      {"@type":"ListItem","position":2,"name":"Services","item":DOMAIN+"/services.html"},
      {"@type":"ListItem","position":3,"name":name,"item":canon}]}, ensure_ascii=False)
    extra_ld = f'<script type="application/ld+json">{ld}</script>\n<script type="application/ld+json">{bc}</script>'

    doc = head(title, desc, canon, "../", og_for(slug), extra_ld)
    doc += nav("../", solid=False, active="services", active_slug=slug)
    doc += f"""
<section class="shero">
  <div class="shero-media" data-img="{slug}" data-i="0" data-alt="{esc(name)} in {CITY}"></div>
  <div class="viewfinder" aria-hidden="true"><span></span><span></span><span></span><span></span><span class="rec"><span class="dot"></span>REC</span></div>
  <div class="wrap shero-inner">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="../services.html">Services</a><span>/</span>{esc(name)}</nav>
    <span class="exif" style="margin-top:1.2rem">{esc(catlabel)}</span>
    <h1>{esc(name)}</h1>
    <p class="shero-sub">{esc(sub)}</p>
    <div class="shero-actions">
      <a class="btn btn--gold" href="../index.html#contact">Book your date</a>
      <a class="btn btn--ghost" href="https://wa.me/{WA}?text={quote(wamsg)}" target="_blank" rel="noopener">WhatsApp us</a>
    </div>
  </div>
</section>

<main id="main">

<section class="section">
  <div class="wrap overview-grid">
    <div class="overview-body">
      <span class="exif">About this service</span>
      <h2>{esc(name)} in {CITY}</h2>
      <p>{esc(p1)}</p>
      <p>{esc(p2)}</p>
      <a class="btn btn--ghost" href="../services.html">Browse all services</a>
    </div>
    <div class="overview-media" data-img="{slug}" data-i="1" data-alt="{esc(name)} sample"></div>
  </div>
</section>

<section class="section section--panel">
  <div class="wrap">
    <div class="sec-head"><span class="exif">What's included</span><h2>What you get</h2>
      <p>Every {esc(name.lower())} booking includes the essentials below. We tailor the exact coverage to your event on a quick call.</p></div>
    <div class="includes-grid">
{inc}
    </div>
  </div>
</section>

<section class="section" id="gallery">
  <div class="wrap">
    <div class="sec-head"><span class="exif">Selected frames · <span data-count-images>loading…</span></span><h2>Recent {esc(name.lower())} work</h2>
      <p>A live selection from recent shoots. Tap any frame to open the full image.</p></div>
    <div class="contact-sheet" data-gallery="{slug}" data-label="{esc(name)}"></div>
  </div>
</section>

<section class="section section--panel">
  <div class="wrap">
    <div class="sec-head"><span class="exif">How it works</span><h2>From enquiry to gallery</h2></div>
    <div class="process">
      <div class="step"><span class="fnum">FRAME 01</span><h3>Enquire</h3><p>Send your date and details. We reply within a day with availability and a rough quote.</p></div>
      <div class="step"><span class="fnum">FRAME 02</span><h3>Consult</h3><p>A quick call or coffee to see full galleries and shape the coverage around you.</p></div>
      <div class="step"><span class="fnum">FRAME 03</span><h3>Shoot</h3><p>We show up prepared, stay unobtrusive, and let the moments happen.</p></div>
      <div class="step"><span class="fnum">FRAME 04</span><h3>Deliver</h3><p>Sneak peeks in 72 hours, the full edited gallery in a few weeks.</p></div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap inner">
    <span class="exif no-rule" style="justify-content:center">Ready when you are</span>
    <h2>Let's plan your {esc(name.lower())}</h2>
    <p>Tell us the date and the shape of your event, and we'll come back within a day with availability and a clear quote.</p>
    <div class="cta-actions">
      <a class="btn btn--gold" href="../index.html#contact">Book a date</a>
      <a class="btn btn--ghost" href="https://wa.me/{WA}?text={quote(wamsg)}" target="_blank" rel="noopener">Chat on WhatsApp</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="exif">You might also want</span><h2>Related services</h2></div>
    <div class="related-grid">
{rel_html}
    </div>
  </div>
</section>

</main>
"""
    doc += footer("../")
    doc += wa_float("../", wamsg)
    return doc

# ---------------- SERVICES HUB ----------------
def hub_page():
    canon = f"{DOMAIN}/services.html"
    title = f"Photography & Videography Services in {CITY} | {BRAND}"
    desc  = f"All {len(ORDER)} photography and videography services by {BRAND} in {CITY} — weddings, maternity, newborn, events, commercial, film, albums and more."
    doc = head(title, desc[:158], canon, "", og_for("wedding-photographers"))
    doc += nav("", solid=True, active="services")
    doc += f"""
<main id="main">
<section class="hub-hero">
  <span class="exif no-rule">{len(ORDER)} services · one studio</span>
  <h1>Everything we shoot</h1>
  <p>From weddings and newborns to product catalogues and corporate films — browse every service below, each with its own gallery. Based in {CITY}, working across Tamil Nadu and beyond.</p>
</section>
<section class="section"><div class="wrap">
"""
    # group by category, in CATS order
    for ckey, cmeta in CATS.items():
        members = [s for s in ORDER if S[s][1]==ckey]
        if not members: continue
        items = "\n".join(
          f'''      <a class="hub-item" href="services/{s}.html"><b>{esc(S[s][0])}</b><span class="arw">→</span></a>'''
          for s in members)
        doc += f"""  <div class="hub-cat">
    <span class="cat-line">{esc(cmeta['label'])} · {len(members)}</span>
    <div class="hub-list">
{items}
    </div>
  </div>
"""
    doc += """</div></section>

<section class="cta-band"><div class="wrap inner">
  <span class="exif no-rule" style="justify-content:center">Not sure which you need?</span>
  <h2>Tell us about your event</h2>
  <p>Message us with what you're planning and we'll point you to the right coverage and a clear quote.</p>
  <div class="cta-actions">
    <a class="btn btn--gold" href="index.html#contact">Get in touch</a>
    <a class="btn btn--ghost" href="https://wa.me/%s" target="_blank" rel="noopener">WhatsApp us</a>
  </div>
</div></section>
</main>
""" % WA
    doc += footer("")
    doc += wa_float("")
    return doc

# ---------------- LEGAL ----------------
def legal_page(kind):
    if kind=="privacy":
        title=f"Privacy Policy | {BRAND}"; h="Privacy Policy"
        body=f"""<p class="note"><b>Draft for review.</b> This policy is a starting point aligned to India's Digital Personal Data Protection Act, 2023. Have it reviewed and insert your real grievance officer's name before publishing.</p>
<h2>What we collect</h2><p>When you use our enquiry form or WhatsApp link we collect the name, phone number, event date and message you provide, solely to respond to your enquiry and plan your booking. Basic analytics identifiers may be collected to understand site usage.</p>
<h2>Basis &amp; consent</h2><p>We process this data on the basis of your consent, given when you submit an enquiry. You may withdraw consent or ask us to delete your data at any time by contacting us.</p>
<h2>Your rights</h2><p>You have the right to access, correct and erase your personal data, to grievance redressal, and to nominate another person to exercise your rights. To exercise any of these, contact our grievance officer below.</p>
<h2>Retention &amp; sharing</h2><p>We keep enquiry data only as long as needed to serve you, and share it only with the tools required to deliver your booking. We do not sell your data.</p>
<h2>Grievance officer</h2><p>[Insert name], {BRAND}, {ADDRESS}. Email: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>"""
    else:
        title=f"Terms of Service | {BRAND}"; h="Terms of Service"
        body=f"""<p class="note"><b>Draft for review.</b> These terms are a starting template. Have them reviewed by a professional before publishing.</p>
<h2>Bookings</h2><p>A date is confirmed only on receipt of the agreed retainer. Retainers are non-refundable as they reserve a date we turn away other work for.</p>
<h2>Deliverables &amp; timelines</h2><p>Delivery timelines are estimates communicated at booking. We deliver a curated, edited set of images and film; raw files are not included unless separately agreed.</p>
<h2>Usage &amp; copyright</h2><p>{BRAND} retains copyright of images created. You receive a personal-use licence to print and share. We may use selected images in our portfolio unless you opt out in writing.</p>
<h2>Liability</h2><p>Our liability is limited to the fees paid for the booking. We are not liable for circumstances beyond our reasonable control.</p>
<h2>Contact</h2><p>{BRAND}, {ADDRESS}. Email: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>"""
    canon=f"{DOMAIN}/{kind}.html"
    doc = head(title, f"{h} for {BRAND}.", canon, "", og_for("wedding-photographers"))
    doc += nav("", solid=True)
    doc += f"""<main id="main"><section class="legal"><div class="wrap">
<span class="exif">Legal</span>
<h1>{h}</h1>
<p class="updated">Last updated · {YEAR}</p>
{body}
</div></section></main>
"""
    doc += footer("")
    doc += wa_float("")
    return doc

# ---------------- HOMEPAGE ----------------
def home_page():
    from urllib.parse import quote
    canon=f"{DOMAIN}/"
    title=f"{BRAND} — Wedding &amp; Film Photography in {CITY}"
    desc=f"{BRAND} is a {CITY} wedding & film studio covering weddings, portraits, maternity, newborn, events and commercial work across Tamil Nadu. 47 services, one team."
    # homepage portfolio: pull a mix with data-cat matching filters
    picks = {
      "weddings":["wedding-photographers","candid-wedding-photography","engagement-photographers"],
      "portraits":["portrait-photography","fashion-photographers","family-shoot"],
      "commercial":["product-e-commerce-photographers","corporate-photographers","drone-photography"],
      "events":["events-photographers","birthday-photographers","baby-shower-photographers"],
    }
    cells=[]; n=1
    for cat, slugs in picks.items():
        for sg in slugs:
            cells.append(f'''      <figure class="frame" data-cat="{cat}" data-img="{sg}" data-i="0" data-alt="{esc(S[sg][0])}"><figcaption><span class="cat">{esc(S[sg][0])}</span><span class="num">FR {n:02d}</span></figcaption></figure>''')
            n+=1
    portfolio = "\n".join(cells)

    # featured 6 services
    feats = [("wedding-photographers",'<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.4"/>'),
             ("pre-wedding-photoshoot",'<path d="M12 3s6 5 6 10a6 6 0 0 1-12 0c0-5 6-10 6-10z"/>'),
             ("newborn-photography",'<circle cx="12" cy="8" r="3.2"/><path d="M5 20c0-3.9 3.1-7 7-7s7 3.1 7 7"/>'),
             ("events-photographers",'<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18"/>'),
             ("product-e-commerce-photographers",'<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M9 5V3h6v2M9 12h6"/>'),
             ("professional-videography",'<path d="M4 5h11v14H4z"/><path d="M15 9l5-2v10l-5-2"/>')]
    fcards=[]
    for i,(sg,ico) in enumerate(feats):
        nm,ct,sb,_,_=S[sg]
        fcards.append(f'''      <article class="service"><span class="idx">{i+1:02d}</span>
        <svg class="ico" viewBox="0 0 24 24">{ico}</svg>
        <h3>{esc(nm)}</h3><p>{esc(sb)}</p>
        <a href="services/{sg}.html">Explore</a></article>''')
    services = "\n".join(fcards)

    doc = head(title, desc[:158], canon, "", og_for("wedding-photographers"))
    doc += nav("", solid=False)
    doc += f"""
<section class="hero">
  <div class="hero-media" data-img="wedding-photographers" data-i="0" data-alt="Wedding couple in golden-hour light, {CITY}"></div>
  <div class="viewfinder" aria-hidden="true"><span></span><span></span><span></span><span></span><span class="rec"><span class="dot"></span>REC</span></div>
  <div class="hero-inner">
    <span class="exif no-rule">{CITY} · est. 2014 · weddings &amp; film</span>
    <h1>We keep the light<br>you keep <em>the day</em></h1>
    <p class="hero-sub">A wedding &amp; film studio for people who want their photographs to feel like the moment, not a pose.</p>
    <div class="hero-actions">
      <a class="btn btn--gold" href="#contact">Book your date</a>
      <a class="btn btn--ghost" href="services.html">All 47 services</a>
    </div>
  </div>
  <div class="hero-readout" aria-hidden="true">
    <span class="exif">ƒ/1.8 · 1/200s · ISO 400</span>
    <span class="scroll-cue">Scroll</span>
    <span class="exif" style="justify-content:flex-end">35mm · golden hour</span>
  </div>
</section>

<main id="main">

<section class="trust" aria-label="Credibility">
  <div class="wrap trust-inner">
    <div class="stat"><b data-count="620">0</b><small>Weddings shot</small></div>
    <div class="trust-divider"></div>
    <div class="stat"><b data-count="11">0</b><small>Years behind the lens</small></div>
    <div class="trust-divider"></div>
    <div class="stat"><b data-count="47" data-suffix="">0</b><small>Services offered</small></div>
    <div class="trust-divider"></div>
    <div class="trust-logos" aria-label="Featured in"><span>WedMeGood</span><span>The Knot</span><span>Vogue Weddings</span></div>
  </div>
</section>

<section class="section" id="work">
  <div class="wrap">
    <div class="folio-top">
      <div class="sec-head" style="margin-bottom:0"><span class="exif">Contact sheet · selected frames</span><h2>Recent work</h2></div>
      <div class="filters" role="group" aria-label="Filter portfolio">
        <button aria-pressed="true" data-filter="all">All</button>
        <button aria-pressed="false" data-filter="weddings">Weddings</button>
        <button aria-pressed="false" data-filter="portraits">Portraits</button>
        <button aria-pressed="false" data-filter="commercial">Commercial</button>
        <button aria-pressed="false" data-filter="events">Events</button>
      </div>
    </div>
    <div class="contact-sheet" id="sheet">
{portfolio}
    </div>
    <div class="folio-more"><a class="btn btn--ghost" href="services.html">Browse services &amp; galleries</a></div>
  </div>
</section>

<section class="section section--panel" id="reel">
  <div class="wrap">
    <div class="sec-head center-head"><span class="exif no-rule">Signature film · 2026 reel</span><h2>One take of what we do</h2>
      <p>Ninety seconds of weddings, portraits and brand films, cut the way we shoot — quiet, warm, unhurried.</p></div>
    <div class="reel-frame" id="reel-frame">
      <span class="reel-caption">HALO &amp; GRAIN — REEL 2026 · 1:34</span>
      <img data-img="elements-resort-prewedding-shoot" data-i="0" width="1600" height="900" alt="Showreel cover frame" loading="lazy">
      <button class="reel-play" id="reelPlay" aria-label="Play showreel"><span class="disc"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span></button>
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <div class="folio-top">
      <div class="sec-head" style="margin-bottom:0"><span class="exif">What we shoot</span><h2>Services</h2></div>
      <a class="btn btn--ghost" href="services.html">All 47 services →</a>
    </div>
    <div class="services-grid">
{services}
    </div>
  </div>
</section>

<section class="section section--panel" id="about">
  <div class="wrap about-grid">
    <div class="about-photo"><img loading="lazy" data-img="fashion-photographers" data-i="1" width="700" height="875" alt="Meera Nathan, lead photographer"><span class="tag">On set · 240 days a year</span></div>
    <div class="about-body">
      <span class="exif">Behind the lens</span>
      <h2>Hi, I'm Meera</h2>
      <p>I started {esc(BRAND)} in a one-room studio in Besant Nagar with a borrowed 50mm and a stubborn belief that the best photographs happen when nobody's performing for the camera.</p>
      <p>Eleven years and a few hundred weddings later, that hasn't changed. We're a small team on purpose — the person you meet at your first coffee is the person shooting your day. We work in warm, honest light and hand you photographs that still feel true a decade from now.</p>
      <p class="sign">Meera Nathan</p>
    </div>
  </div>
</section>

<section class="section" id="stories">
  <div class="wrap">
    <div class="sec-head"><span class="exif">In their words</span><h2>Couples &amp; clients</h2></div>
    <div class="quotes">
      <figure class="quote"><div class="stars" aria-label="5 out of 5">★★★★★</div>
        <blockquote>They were invisible all day and then handed us photos that made us cry. It felt like reliving the wedding, not reviewing it.</blockquote>
        <figcaption class="who"><img loading="lazy" data-img="portrait-photography" data-i="0" width="88" height="88" alt=""><span><b>Aishwarya &amp; Karthik</b><small>Wedding · Mahabalipuram</small></span></figcaption></figure>
      <figure class="quote is-video"><span class="vtag">Video testimonial</span>
        <blockquote>The brand film they cut for our launch outperformed every ad we'd run. Same team, start to finish, no fuss.</blockquote>
        <figcaption class="who"><img loading="lazy" data-img="corporate-photographers" data-i="1" width="88" height="88" alt=""><span><b>Priya Menon</b><small>Founder · Studio Svasa</small></span></figcaption></figure>
      <figure class="quote"><div class="stars" aria-label="5 out of 5">★★★★★</div>
        <blockquote>Booked them for a portrait session and ended up booking the whole wedding. You just trust the way they see.</blockquote>
        <figcaption class="who"><img loading="lazy" data-img="family-shoot" data-i="2" width="88" height="88" alt=""><span><b>Rohan Iyer</b><small>Portrait · Chennai</small></span></figcaption></figure>
    </div>
  </div>
</section>

<section class="section section--panel" id="pricing">
  <div class="wrap">
    <div class="sec-head center-head"><span class="exif no-rule">Transparent packages</span><h2>Pricing</h2>
      <p>Every package includes both photo and a highlight film. Custom quotes for multi-day and destination events.</p></div>
    <div class="tiers">
      <article class="tier"><h3>The Session</h3><div class="price">₹35,000<small> starting</small></div>
        <ul><li>Up to 4 hours coverage</li><li>One photographer</li><li>60+ edited photographs</li><li>60-second highlight reel</li><li>Online gallery, 12 months</li></ul>
        <a class="btn btn--ghost" href="#contact">Enquire</a></article>
      <article class="tier tier--feature"><h3>The Wedding Day</h3><div class="price">₹1,25,000<small> starting</small></div>
        <ul><li>Full-day photo &amp; film</li><li>Two shooters + assistant</li><li>400+ edited photographs</li><li>3–4 min cinematic film</li><li>Premium album + gallery</li></ul>
        <a class="btn btn--gold" href="#contact">Check your date</a></article>
      <article class="tier"><h3>The Celebration</h3><div class="price">₹2,40,000<small> starting</small></div>
        <ul><li>Multi-day / destination</li><li>Full team + drone</li><li>800+ edited photographs</li><li>Feature film + teasers</li><li>Two albums + prints</li></ul>
        <a class="btn btn--ghost" href="#contact">Request a quote</a></article>
    </div>
    <p class="price-note">Dates book 6–12 months ahead. A 25% retainer holds your date; balance on delivery.</p>
  </div>
</section>

<section class="section" id="faq">
  <div class="wrap">
    <div class="sec-head center-head"><span class="exif no-rule">Good to know</span><h2>Frequently asked</h2></div>
    <div class="faq">
      <details open><summary>How soon do we get our photos?</summary><p>Sneak-peek edits land within 72 hours. The full edited gallery is ready in 4–6 weeks, and cinematic films follow 2–3 weeks after that. Rush delivery is available on request.</p></details>
      <details><summary>Do you travel? What about outstation charges?</summary><p>Yes — we shoot across Tamil Nadu, Pondicherry, Bengaluru and destination weddings anywhere. Travel and stay are billed at actuals for events beyond 40 km from {CITY}, agreed in writing before booking.</p></details>
      <details><summary>What deposit do you need to hold a date?</summary><p>A 25% retainer confirms and blocks your date. The balance is split — a portion before the shoot and the remainder on final delivery.</p></details>
      <details><summary>Do we get the raw, unedited files?</summary><p>We deliver a fully culled and colour-graded gallery rather than raw files — it's the work at its best. Raw files can be licensed separately if you specifically need them.</p></details>
      <details><summary>Is there a backup shooter and backup of our files?</summary><p>Always. Every wedding is covered by at least two shooters, all cameras record to dual cards, and your files are backed up to three locations until final delivery.</p></details>
    </div>
  </div>
</section>

<section class="section section--panel" id="contact">
  <div class="wrap contact-grid">
    <div class="contact-copy">
      <span class="exif">Let's talk</span>
      <h2>Tell us about your day</h2>
      <p>Share the date and the shape of your event. We'll come back within a day — and if we're already booked, we'll point you to someone we trust.</p>
      <div class="lines">
        <a href="tel:{PHONE_TEL}" data-href="tel"><span class="k">Call</span> <span data-b="phone">{PHONE_DISP}</span></a>
        <a href="mailto:{EMAIL}" data-href="mail"><span class="k">Email</span> <span data-b="email">{EMAIL}</span></a>
        <span><span class="k">Studio</span> <span data-b="address">{ADDRESS}</span></span>
      </div>
      <a class="btn btn--gold wa-cta" href="https://wa.me/{WA}?text={quote('Hi Halo & Grain, I would like to check your availability for my event.')}" target="_blank" rel="noopener">Chat on WhatsApp</a>
    </div>
    <div class="form">
      <div class="field"><label for="f-name">Your name</label><input id="f-name" type="text" autocomplete="name" placeholder="e.g. Aishwarya"></div>
      <div class="field"><label for="f-date">Event date</label><input id="f-date" type="date"></div>
      <div class="field"><label for="f-type">Event type</label>
        <select id="f-type"><option>Wedding</option><option>Pre-wedding shoot</option><option>Maternity / Newborn</option><option>Birthday / Event</option><option>Commercial / Brand</option><option>Other</option></select></div>
      <div class="field"><label for="f-msg">A little about it</label><textarea id="f-msg" placeholder="City, guest count, what you're picturing…"></textarea></div>
      <button class="btn btn--gold" id="sendWa" type="button" data-wa="{WA}">Send enquiry via WhatsApp</button>
      <p class="form-note">Opens WhatsApp with your details pre-filled — no account needed.</p>
    </div>
  </div>
</section>

</main>
"""
    doc += footer("")
    doc += wa_float("")
    return doc

# ---------------- SITEMAP / ROBOTS ----------------
def sitemap():
    urls=[DOMAIN+"/", DOMAIN+"/services.html", DOMAIN+"/privacy.html", DOMAIN+"/terms.html"]
    urls += [f"{DOMAIN}/services/{s}.html" for s in ORDER]
    items="\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'

def robots():
    return f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n"

# ---------------- IMAGE MANIFEST + FALLBACK + AUTOMATION ----------------
def build_manifest_data():
    cats = []
    for s in ORDER:
        files = FILES.get(s, [])
        cats.append({"slug": s, "title": S[s][0], "files": files})
    return {"generated": "baked", "categories": cats}

MANIFEST = build_manifest_data()

# TITLES dict for the standalone build script (display names per slug)
TITLES_PY = json.dumps({s: S[s][0] for s in ORDER}, ensure_ascii=False, indent=0)

BUILD_SCRIPT = '''#!/usr/bin/env python3
# Rebuild manifest.json + assets/js/images-data.js from whatever is in images/.
# Run locally (python3 build-manifest.py) or let the GitHub Action run it on push.
import os, re, json, datetime

IMAGES_DIR = "images"
IMG_RE = re.compile(r"\\.(?:jpe?g|png|webp|gif|avif)$", re.I)
TITLES = %s

def natural_key(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\\d+)", name)]

def title_from_slug(slug):
    return " ".join(w.capitalize() for w in re.split(r"[-_]+", slug) if w)

cats = []
if os.path.isdir(IMAGES_DIR):
    for slug in sorted(os.listdir(IMAGES_DIR)):
        d = os.path.join(IMAGES_DIR, slug)
        if not os.path.isdir(d):
            continue
        files = sorted((f for f in os.listdir(d) if IMG_RE.search(f)), key=natural_key)
        if files:
            cats.append({"slug": slug, "title": TITLES.get(slug, title_from_slug(slug)), "files": files})

data = {"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(), "categories": cats}
with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
os.makedirs("assets/js", exist_ok=True)
with open("assets/js/images-data.js", "w", encoding="utf-8") as f:
    f.write("window.IMAGES_DATA=" + json.dumps(data, ensure_ascii=False) + ";")
print("Rebuilt manifest:", len(cats), "folders,",
      sum(len(c["files"]) for c in cats), "images")
''' % TITLES_PY

WORKFLOW = '''name: Build image manifest
on:
  push:
    paths:
      - "images/**"
      - "build-manifest.py"
      - ".github/workflows/build-manifest.yml"
  workflow_dispatch:
permissions:
  contents: write
concurrency:
  group: build-manifest
  cancel-in-progress: true
jobs:
  manifest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Rebuild manifest from images/
        run: python3 build-manifest.py
      - name: Commit if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add manifest.json assets/js/images-data.js
          git diff --cached --quiet || git commit -m "chore: rebuild image manifest [skip ci]"
          git push
'''

README = '''# Halo & Grain — photography & videography website

Static multi-page site (plain HTML/CSS/JS, no build step) for GitHub Pages.
Images are loaded **dynamically** from the site's own `images/` folder — add,
rename or delete a photo and the site keeps working, with no blank boxes.

## How the dynamic gallery works
1. Put photos in `images/<service-slug>/` (one subfolder per service — the
   slugs match the service page filenames in `services/`).
2. On every push that touches `images/**`, the GitHub Action
   (`.github/workflows/build-manifest.yml`) runs `build-manifest.py`, which
   rescans `images/` and rewrites `manifest.json` + `assets/js/images-data.js`.
3. In the browser, `assets/js/gallery.js` fetches `manifest.json` and renders
   every gallery, hero and thumbnail from it. Each `<img>` has an error guard,
   so a just-deleted / renamed file is never shown as a broken image.

So: **you only ever add/remove files in `images/<slug>/` and push.** No lists to
maintain by hand, no API, no cost.

### First-time setup (one time)
- Enable the Action: repo *Settings -> Actions -> General -> Workflow
  permissions -> Read and write*, then push once (or run the workflow manually).
- Or skip Actions entirely and run `python3 build-manifest.py` locally whenever
  you change images, then commit the regenerated `manifest.json`.

### Folder -> service slugs
Each folder name must match a service page, e.g. `images/wedding-photographers/`,
`images/newborn-photography/`, `images/drone-photography/`. Full list is in
`manifest.json`.

## Before launch
- Replace `https://example.com` with your real domain (canonical/OG/sitemap).
- Replace the placeholder phone / email / studio address (keep them identical
  to your Google Business Profile).
- Finish the `privacy.html` / `terms.html` drafts (add a real grievance officer).

## Regenerate the pages themselves
`gen.py` (kept in this archive) builds all the HTML pages. Run `python3 gen.py`
after editing copy. It does **not** touch `images/` — that stays yours.
'''

# ---------------- WRITE ----------------
def w(path, content):
    full=os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full,"w",encoding="utf-8").write(content)

w("index.html", home_page())
w("services.html", hub_page())
w("privacy.html", legal_page("privacy"))
w("terms.html", legal_page("terms"))
w("sitemap.xml", sitemap())
w("robots.txt", robots())
for s in ORDER:
    w(f"services/{s}.html", service_page(s))

# manifest + baked fallback (starting state; the Action keeps them fresh)
w("manifest.json", json.dumps(MANIFEST, ensure_ascii=False))
w("assets/js/images-data.js", "window.IMAGES_DATA=" + json.dumps(MANIFEST, ensure_ascii=False) + ";")
# automation + docs
w("build-manifest.py", BUILD_SCRIPT)
w(".github/workflows/build-manifest.yml", WORKFLOW)
w("README.md", README)
# a note in images/ so the folder ships even before the user drops photos in
w("images/README.txt",
  "Put photos here as images/<service-slug>/<file>.jpg\n"
  "e.g. images/wedding-photographers/001.jpg\n"
  "Folder names must match the service page slugs (see manifest.json).\n"
  "Add / rename / delete freely, then push — the manifest rebuilds automatically.\n")

print("Generated:", 6 + len(ORDER), "pages + manifest, fallback, Action, README")
print(" -", len(ORDER), "service pages")
print(" - images:", sum(len(v) for v in FILES.values()), "across", len(FILES), "folders (in manifest)")

# =====================================================================
# MULTI-TENANT BRANDING CONFIG  (one repo, per-customer ?c=slug)
# =====================================================================
DEFAULT_BRAND = {
    "name": BRAND,
    "phone": PHONE_DISP,
    "whatsapp": WA,
    "email": EMAIL,
    "address": ADDRESS,
    "city": CITY,
    "instagram": "https://www.instagram.com/",
    "youtube": "https://www.youtube.com/",
    "facebook": "",
    "colorPrimary": "#D9B26A",
    "colorPrimaryBright": "#EAC988",
    "colorPrimaryDeep": "#B8894A",
    "colorInk": "#14110E",
    "font": "'Helvetica Neue', Helvetica, Arial, sans-serif",
    "googleFont": ""
}

# two sample customers so demos work out of the box
SAMPLE_CUSTOMERS = {
    "sunrise-studio": {
        "name": "Sunrise Studio", "phone": "+91 90000 11111", "whatsapp": "919000011111",
        "email": "hello@sunrisestudio.example", "city": "Coimbatore",
        "address": "12 Race Course Road, Coimbatore, Tamil Nadu 641018",
        "instagram": "https://www.instagram.com/", "youtube": "https://www.youtube.com/",
        "colorPrimary": "#E0873C", "colorInk": "#161210", "googleFont": ""
    },
    "azure-films": {
        "name": "Azure Films", "phone": "+91 90000 22222", "whatsapp": "919000022222",
        "email": "studio@azurefilms.example", "city": "Bengaluru",
        "address": "5 Church Street, Bengaluru, Karnataka 560001",
        "instagram": "https://www.instagram.com/", "youtube": "https://www.youtube.com/",
        "colorPrimary": "#5B8CB0", "colorInk": "#0F1417", "googleFont": ""
    }
}

CUSTOMERS_JSON = json.dumps({"_default": DEFAULT_BRAND, "customers": SAMPLE_CUSTOMERS},
                            ensure_ascii=False, indent=2)

# CSV template (edit in Excel / Google Sheets, export, run build-config.py)
_cols = ["slug","name","phone","whatsapp","email","address","city",
         "instagram","youtube","facebook","colorPrimary","colorInk","font","googleFont"]
def _csv_row(slug, d):
    vals = [slug] + [str(d.get(k, "")) for k in _cols[1:]]
    return ",".join('"' + v.replace('"', '""') + '"' for v in vals)
CUSTOMERS_CSV = "\n".join(
    [",".join(_cols),
     _csv_row("_default", DEFAULT_BRAND)] +
    [_csv_row(s, {**DEFAULT_BRAND, **d}) for s, d in SAMPLE_CUSTOMERS.items()]
) + "\n"

BUILD_CONFIG = '''#!/usr/bin/env python3
# Convert config/customers.csv  ->  config/customers.json
# Maintain the CSV in Excel or Google Sheets (File > Download > .csv),
# drop it in config/, then run:  python3 build-config.py
# (or let the GitHub Action do it automatically on push).
import csv, json, os

CSV_PATH  = os.path.join("config", "customers.csv")
JSON_PATH = os.path.join("config", "customers.json")
BOOL_EMPTY = ("", None)

def clean(row):
    return {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k}

with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
    rows = [clean(r) for r in csv.DictReader(f)]

default = {}
customers = {}
for r in rows:
    slug = (r.get("slug") or "").strip()
    if not slug:
        continue
    data = {k: v for k, v in r.items() if k != "slug" and v not in BOOL_EMPTY}
    if slug == "_default":
        default = data
    else:
        customers[slug] = data

out = {"_default": default, "customers": customers}
os.makedirs("config", exist_ok=True)
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("Wrote", JSON_PATH, "-", len(customers), "customers")
'''

CONFIG_WORKFLOW = '''name: Build customers config
on:
  push:
    paths:
      - "config/customers.csv"
      - "build-config.py"
      - ".github/workflows/build-config.yml"
  workflow_dispatch:
permissions:
  contents: write
concurrency:
  group: build-config
  cancel-in-progress: true
jobs:
  config:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Convert customers.csv -> customers.json
        run: python3 build-config.py
      - name: Commit if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add config/customers.json
          git diff --cached --quiet || git commit -m "chore: rebuild customers config [skip ci]"
          git push
'''

# a private index of demo links (not in nav) — reads customers.json at runtime
DEMOS = f'''<!DOCTYPE html>
<html lang="en-IN"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Demo links · {esc(BRAND)}</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="assets/css/main.css">
<style>
  body{{padding:6rem var(--gutter) 4rem;}}
  .demos{{width:min(100% - 2*var(--gutter), 900px); margin-inline:auto;}}
  .demos h1{{font-size:var(--step-3); margin-bottom:.4rem;}}
  .demos p.lead{{margin:0 0 2.5rem; color:var(--cream-dim);}}
  .demo-row{{display:flex; align-items:center; justify-content:space-between; gap:1rem; flex-wrap:wrap;
    padding:1.1rem 1.3rem; background:var(--ink-2); border:1px solid var(--line); border-radius:var(--radius); margin-bottom:.6rem;}}
  .demo-row .sw{{width:22px;height:22px;border-radius:50%;flex:none;border:1px solid var(--line-2);}}
  .demo-row .meta{{display:flex;align-items:center;gap:.9rem;min-width:0;}}
  .demo-row b{{color:var(--cream);font-weight:600;}}
  .demo-row code{{font-family:var(--font-mono);font-size:.8rem;color:var(--cream-dim);}}
  .demo-row .act{{display:flex;gap:.5rem;}}
  .demo-row a.open,.demo-row button.copy{{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;
    border:1px solid var(--line-2);border-radius:var(--radius);padding:.5rem .8rem;color:var(--cream);background:none;cursor:pointer;}}
  .demo-row a.open:hover,.demo-row button.copy:hover{{border-color:var(--gold);color:var(--gold-bright);}}
</style></head>
<body data-root="">
<div class="demos">
  <span class="exif no-rule">Internal · not indexed</span>
  <h1>Customer demo links</h1>
  <p class="lead">Each customer sees the site with their own branding at their unique URL. Share the link; nothing else changes.</p>
  <div id="list">Loading…</div>
</div>
<script>
(function(){{
  var base = location.href.replace(/demos\\.html.*$/, "index.html");
  fetch("config/customers.json",{{cache:"no-cache"}}).then(function(r){{return r.json();}}).then(function(cfg){{
    var def = cfg._default||{{}}, cs = cfg.customers||{{}}, host = document.getElementById("list");
    var keys = Object.keys(cs);
    if(!keys.length){{ host.textContent = "No customers yet — add rows to config/customers.csv."; return; }}
    host.innerHTML = "";
    keys.forEach(function(slug){{
      var c = Object.assign({{}}, def, cs[slug]);
      var url = base + "?c=" + slug;
      var row = document.createElement("div"); row.className = "demo-row";
      var meta = document.createElement("div"); meta.className = "meta";
      var sw = document.createElement("span"); sw.className = "sw"; sw.style.background = c.colorPrimary || "#D9B26A";
      var name = document.createElement("b"); name.textContent = c.name || slug;
      var code = document.createElement("code"); code.textContent = "?c=" + slug;
      meta.appendChild(sw); meta.appendChild(name); meta.appendChild(code);
      var act = document.createElement("div"); act.className = "act";
      var open = document.createElement("a"); open.className = "open"; open.href = url; open.target = "_blank"; open.textContent = "Open";
      var copy = document.createElement("button"); copy.className = "copy"; copy.textContent = "Copy link";
      copy.onclick = function(){{ navigator.clipboard.writeText(url).then(function(){{ copy.textContent="Copied"; setTimeout(function(){{copy.textContent="Copy link";}},1200); }}); }};
      act.appendChild(open); act.appendChild(copy);
      row.appendChild(meta); row.appendChild(act); host.appendChild(row);
    }});
  }}).catch(function(){{ document.getElementById("list").textContent = "Could not load config/customers.json"; }});
}})();
</script>
</body></html>'''

w("config/customers.json", CUSTOMERS_JSON)
w("config/customers.csv", CUSTOMERS_CSV)
w("build-config.py", BUILD_CONFIG)
w(".github/workflows/build-config.yml", CONFIG_WORKFLOW)
w("demos.html", DEMOS)

print("Branding: config/customers.json (+csv), build-config.py, demos.html, config Action")
