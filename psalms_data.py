# Psalm meaning pages: one page per psalm people search ("psalm 131 meaning").
# First set: the Songs of Ascent, Psalms 120 to 134, drawn from the Incense & Oil
# series (Oct 2026) and the Songs of Ascent reading plan notes.
# Each page: short answer, the full psalm (WEB, from psalms_web.json), the meaning,
# where it fits in the climb, a question, a prayer, and links to our teaching.
# body = HTML. blog = post slug or None. video = (YouTube id, title) or None. plans = plan slugs.

SOA_INTRO = ("The Songs of Ascent are Psalms 120 to 134, fifteen short songs that pilgrims sang on the way up to "
             "Jerusalem for the great feasts. Each one carries the title \"A Song of Ascents.\" Read together, they "
             "trace one journey: from distress far from home (Psalm 120) to blessing in the house of the Lord (Psalm 134).")

V1 = ("_88vD2fSZvI", "Incense & Oil, Part 1: The Desire to Go Up")
V2 = ("IrjdjNYg8_8", "Incense & Oil, Part 2: The Snare Is Broken")
V3 = ("JKpVb4ezoRo", "Incense & Oil, Part 3: A Quieted Soul")
V4 = ("bySW8AfGMSY", "Incense & Oil, Part 4: Unity Releases Blessing")

PSALMS = [
 dict(n=120, title="Far From Home", by="Anonymous",
  answer="Psalm 120 is the first of the Songs of Ascent, and it begins the climb in distress. The pilgrim lives among liars and people who love war, cries out to the Lord for rescue, and longs for peace. Every journey toward God starts here: an honest dissatisfaction with where you are that turns you toward Him.",
  body="""
<h2>What Psalm 120 means</h2>
<p>The song opens with a cry: "In my distress, I cried to Yahweh. He answered me." The pilgrim is surrounded by lying lips and deceitful tongues, and the words of others cut like sharp arrows and burn like coals of juniper.</p>
<p>Then comes a strange line: "Woe is me, that I live in Meshech, that I dwell among the tents of Kedar!" Meshech was a people far to the north, and Kedar a tribe of the Arabian desert. No one could live in both places at once. The names paint a picture of living among hostile people wherever you happen to be.</p>
<p>The psalm ends with the line to hold onto: "I am for peace, but when I speak, they are for war."</p>

<h2>Why the climb starts here</h2>
<p>Eugene Peterson pointed out that every pilgrimage begins with a dissatisfaction with where you are. You don't set out for Jerusalem if you are content in Kedar. Lament comes before praise. The first song of the climb is an honest naming of where you are, and that honesty is what turns your feet toward God.</p>
<p>Notice where this goes. The pilgrim who says "I am for peace" in Psalm 120 will pray for the peace of Jerusalem in Psalm 122, the city whose very name means peace.</p>""",
  prompt="Where do you feel far from home right now?",
  prayer="Lord, I am tired of the noise, the lies and the conflict around me. I bring You my distress, because You answer those who cry out to You. Turn my heart toward Your presence and set my feet on the road home. In Jesus' name, amen.",
  blog=None, video=None, plans=[]),

 dict(n=121, title="Where Does My Help Come From?", by="Anonymous",
  answer="Psalm 121 is a Song of Ascents about God's protection on the journey. The pilgrim looks up at the dangerous hills and asks where help will come from, and the answer is the Lord, the Maker of heaven and earth, who never sleeps. The word \"keep\" appears six times: God keeps your life, your soul, and your going out and coming in, forever.",
  body="""
<h2>What Psalm 121 means</h2>
<p>Jerusalem sits high in the Judean hills, so the hills are where the pilgrim is headed. They are also where the road gets steep and dangerous. "I will lift up my eyes to the hills. Where does my help come from?" is the honest question of someone who knows the road ahead is hard.</p>
<p>The answer comes right away: "My help comes from Yahweh, who made heaven and earth." Help does not come from the hills themselves. It comes from the One who made them.</p>
<p>Watch how the voice shifts. Verses 1 and 2 say "I" and "my." Verses 3 to 8 say "you." Many read the psalm as a conversation: a traveler's question answered by a companion, a parent, or a priest speaking a blessing over someone setting out. And six times the answer uses one word: <em>keep</em>. He keeps you. He will not slumber. He keeps your going out and your coming in.</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>Psalm 120 left home. Psalm 121 is on the road. The confession "My help comes from Yahweh, who made heaven and earth" returns in Psalm 124 and again in the very last verse of the collection, Psalm 134. The language of keeping also echoes the priestly blessing: "Yahweh bless you, and keep you" (Numbers 6:24). For centuries this psalm has been spoken over travelers as a blessing for the road.</p>""",
  prompt="What would change if you believed God was keeping your going out and your coming in?",
  prayer="Father, when I look at the hills in front of me, I remember that my help comes from You, the Maker of heaven and earth. Thank You that You never sleep and never stop keeping me. Keep my going out and my coming in today and forever. In Jesus' name, amen.",
  blog="where-does-my-help-come-from", video=None, plans=["where-does-my-help-come-from"]),

 dict(n=122, title="I Was Glad", by="David",
  answer="Psalm 122 is David's song of arriving at Jerusalem. It begins with joy at the invitation, \"Let's go to Yahweh's house,\" celebrates the city bound firmly together, and ends with a prayer for the peace of Jerusalem. It teaches that the joy of worship begins when someone says \"let us go,\" and that God's people are called to pray for the peace of their city.",
  body="""
<h2>What Psalm 122 means</h2>
<p>"I was glad when they said to me, 'Let's go to Yahweh's house!'" The gladness begins at the invitation, before anyone arrives. Then the pilgrim is there: "Our feet are standing within your gates, Jerusalem."</p>
<p>The city is "built as a city that is compact together." The tribes go up to give thanks, and the thrones of David's house are set for justice. Finally the pilgrim prays: "Pray for the peace of Jerusalem." The Hebrew word is <em>shalom</em>: wholeness, nothing missing and nothing broken.</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>In Psalm 120 the pilgrim said, "I am for peace, but when I speak, they are for war." Here, at last, he prays peace over the city whose very name means peace. "Yahweh's house" in verse 1 opens a bracket that closes in Psalm 134, the last step of the climb, where God's servants stand by night in the house of the Lord.</p>
<p>This psalm was likely sung at the gates on arrival. It is a reminder that every invitation to worship matters. Someone said "let us go," and joy followed.</p>""",
  prompt="Who invited you to go up to the house of the Lord, and who could you invite?",
  prayer="Lord, thank You for the people who invited me into Your house. Make me glad to worship You, and make me someone who invites others. I pray for the peace of my city: wholeness, nothing missing and nothing broken. In Jesus' name, amen.",
  blog="the-desire-to-go-up", video=V1, plans=["gladness-in-god"]),

 dict(n=123, title="Looking Up", by="Anonymous",
  answer="Psalm 123 is a short Song of Ascents about attentive dependence on God. The pilgrim lifts their eyes to God enthroned in heaven, like a servant watching the hand of their master, and asks for mercy three times after enduring the contempt of the proud. It teaches us to keep our eyes on God and wait on Him.",
  body="""
<h2>What Psalm 123 means</h2>
<p>"To you I do lift up my eyes, you who sit in the heavens." Arriving in Jerusalem does not end the need. The pilgrim looks past the city to the throne of God.</p>
<p>The picture is of a servant watching the hand of their master, or a maid watching the hand of her mistress, waiting for the smallest signal. That is how the pilgrim waits on God: eyes up, attentive, dependent, until He shows mercy.</p>
<p>Then the cry comes three times: have mercy on us, have mercy on us, for we have had more than enough of contempt. The scorn of the comfortable and the proud has worn them down.</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>In Psalm 121 the eyes went up to the hills. Here they go past the hills and the city to God Himself. This is the posture the whole climb is forming: before we arrive and after we arrive, we keep looking to Him.</p>""",
  prompt="Where are you waiting on the hand of God right now?",
  prayer="Lord, I lift my eyes to You. Like a servant watching for a signal, I am waiting on You. Have mercy on me. When I am worn down by the scorn of others, let my eyes stay fixed on You. In Jesus' name, amen.",
  blog=None, video=None, plans=[]),

 dict(n=124, title="The Snare Is Broken", by="David",
  answer="Psalm 124 is David's song of deliverance. Its message is simple: if the Lord had not been on our side, we would have been swallowed up, but the snare is broken and we have escaped. It ends with a confession Christians still use to open worship: \"Our help is in Yahweh's name, who made heaven and earth.\"",
  body="""
<h2>What Psalm 124 means</h2>
<p>"If it had not been Yahweh who was on our side, let Israel now say." That second line is a cue. A leader sings the first line, and the whole crowd answers. This is a song of a people remembering together.</p>
<p>The images pile up. Enemies who would have swallowed us alive. A flood that would have swept us away. Raging waters up to our necks. A bird caught in a fowler's trap. And then: "The snare is broken, and we have escaped."</p>
<p>The psalm ends with the confession: "Our help is in Yahweh's name, who made heaven and earth." For centuries Christians have opened worship services with this exact line.</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>Having arrived, the pilgrims look back and ask how they got here. Psalm 124 answers first with deliverance. Its last line repeats the confession of Psalm 121:2. This is worship as response: praise that grows out of remembering what God rescued us from.</p>""",
  prompt="Finish the sentence: If it had not been the Lord, I would...",
  prayer="Lord, if You had not been on my side, I would have been swept away. Thank You for every snare You have broken and every flood You have held back. My help is in Your name, Maker of heaven and earth. In Jesus' name, amen.",
  blog="the-snare-is-broken", video=V2, plans=[]),

 dict(n=125, title="Like Mount Zion", by="Anonymous",
  answer="Psalm 125 is a Song of Ascents about security in God. Those who trust in the Lord are like Mount Zion, which cannot be moved, and as the mountains surround Jerusalem, the Lord surrounds His people. It promises that evil will not rule forever over the righteous and ends with a blessing of peace.",
  body="""
<h2>What Psalm 125 means</h2>
<p>"Those who trust in Yahweh are as Mount Zion, which can't be moved, but remains forever." The pilgrim is standing in Jerusalem, looking at the ridges around the city. "As the mountains surround Jerusalem, so Yahweh surrounds his people."</p>
<p>The landscape becomes a sermon. Look at what surrounds you and let it preach God's faithfulness. The psalm also promises that the scepter of wickedness will not rest forever on the land of the righteous, so that they are not pushed into doing evil themselves.</p>
<p>It ends with a blessing: "Peace be on Israel."</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>Rescue in Psalm 124 becomes security in Psalm 125. The same closing blessing, "Peace be on Israel," returns at the end of Psalm 128.</p>""",
  prompt="What makes you feel movable right now, and what would it look like to trust like Mount Zion?",
  prayer="Lord, surround me the way the mountains surround Jerusalem. When I feel shaken, make me steady like Mount Zion. I trust You to hold me and to bring Your peace. In Jesus' name, amen.",
  blog=None, video=None, plans=[]),

 dict(n=126, title="Those Who Sow in Tears", by="Anonymous",
  answer="Psalm 126 is a Song of Ascents about restoration. It remembers when the Lord restored Zion and His people were like those who dream, full of laughter and joy, and then asks God to do it again. Its promise is one of the most loved in Scripture: \"Those who sow in tears will reap in joy.\"",
  body="""
<h2>What Psalm 126 means</h2>
<p>"When Yahweh brought back those who returned to Zion, we were like those who dream. Then our mouth was filled with laughter, and our tongue with singing." Even the nations noticed: the Lord has done great things for them.</p>
<p>The psalm has two halves. Verses 1 to 3 remember a restoration. Verses 4 to 6 ask God to do it again: "Restore our fortunes again, Yahweh, like the streams in the Negev." The streams of the Negev are dry desert beds that flash full when the rains come.</p>
<p>Then the promise: "Those who sow in tears will reap in joy. He who goes out weeping, carrying seed for sowing, will certainly come again with joy, carrying his sheaves."</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>This is the clearest echo of Israel's return from exile in the whole collection, and it closes the first seven songs. Joy and tears sit side by side. The Feast of Tabernacles was a harvest feast, so the image of carrying sheaves home with singing would have been right in front of the pilgrims.</p>""",
  prompt="What are you sowing in tears, and what would it mean to expect a harvest?",
  prayer="Lord, You have done great things before, and I ask You to do them again. Like streams in the desert, restore what has run dry. I give You the seeds I am sowing in tears, and I trust You for a harvest of joy. In Jesus' name, amen.",
  blog=None, video=None, plans=[]),

 dict(n=127, title="Unless the Lord Builds the House", by="Solomon",
  answer="Psalm 127 is Solomon's Song of Ascents and the center of the collection. It teaches that unless the Lord builds the house, the builders labor in vain, and that God gives sleep to those He loves. It is a psalm against anxiety and striving: rest, even sleep, becomes an act of trust, and children are a heritage from the Lord.",
  body="""
<h2>What Psalm 127 means</h2>
<p>"Unless Yahweh builds the house, they labor in vain who build it. Unless Yahweh watches over the city, the watchman guards it in vain." Solomon built the first temple, and here he says the builders' work is empty without God.</p>
<p>Rising early and staying up late, eating the bread of anxious toil, is pointless "for he gives sleep to his loved ones." The Hebrew word for beloved, <em>yedid</em>, echoes Solomon's other name, Jedidiah, which means beloved of the Lord (2 Samuel 12:25).</p>
<p>Then the psalm turns to children: a heritage from the Lord, a reward, like arrows in the hand of a warrior.</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>Psalm 127 is the hinge of the whole climb, with seven songs before it and seven after. The house, the city and the sons here point across the collection: the house of the Lord (122:1 and 134:1), Jerusalem (122:3), and the sons of David (132:11-12). Everything before this psalm says God did it. Everything after builds on that.</p>""",
  prompt="Where are you laboring in vain, building something God has not asked you to build alone?",
  prayer="Lord, build my house, my work and my family. I lay down my anxious striving. Teach me to rest and to sleep in peace, trusting that You watch over what matters most. In Jesus' name, amen.",
  blog=None, video=None, plans=[]),

 dict(n=128, title="Blessed Around the Table", by="Anonymous",
  answer="Psalm 128 is a Song of Ascents about the blessing of a home that fears the Lord. Those who walk in God's ways will eat the fruit of their labor, with a spouse like a fruitful vine and children like olive shoots around the table. The blessing then widens from the home to the whole city of God.",
  body="""
<h2>What Psalm 128 means</h2>
<p>"Blessed is everyone who fears Yahweh, who walks in his ways." The blessing lands at home: you will eat the fruit of your labor, your wife will be like a fruitful vine, and your children like olive shoots around your table.</p>
<p>Then it widens: "May Yahweh bless you out of Zion, and may you see the good of Jerusalem all the days of your life." The home and the house of God are bound together. The psalm ends with the same blessing as Psalm 125: "Peace be upon Israel."</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>Psalm 127 said labor without God is in vain and children are a heritage. Psalm 128 shows the other side: labor blessed and a table full. The Book of Common Prayer has used this psalm in the wedding service for centuries.</p>""",
  prompt="Who is around your table, and how could you bless them this week?",
  prayer="Lord, teach me to fear You and walk in Your ways. Bless my home and the people around my table. Let what happens in my house overflow into blessing for my church and my city. In Jesus' name, amen.",
  blog=None, video=None, plans=[]),

 dict(n=129, title="Plowed But Not Overcome", by="Anonymous",
  answer="Psalm 129 is a Song of Ascents about surviving affliction. Israel has been oppressed from its youth, as if plowers plowed long furrows on its back, yet its enemies have not prevailed. The Lord cuts the cords of the wicked. It teaches that surviving is itself a testimony of God's faithfulness.",
  body="""
<h2>What Psalm 129 means</h2>
<p>"Many times they have afflicted me from my youth up. Let Israel now say." Like Psalm 124, a leader calls and the people answer. The image is brutal: "The plowers plowed on my back. They made their furrows long." And yet: "they have not prevailed against me."</p>
<p>The Lord is righteous, and He has cut apart the cords of the wicked. The psalm ends with an image of grass on a rooftop that withers before anyone can harvest it, and a blessing that no one speaks over the enemies of Zion.</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>Notice the contrast with Psalm 128. The righteous are blessed at their tables, while the enemies of Zion get no blessing at all. Then the songs get honest: long affliction here, sin and waiting in the dark in Psalm 130, and finally a soul calmed and quieted in Psalm 131. A people remembers its suffering together and confesses that it was not the end.</p>""",
  prompt="What has tried to plow you under, and how has God kept you?",
  prayer="Lord, there have been seasons that felt like plows on my back. But I am still here, because You have kept me. Thank You that the cords of the enemy do not have the final word. In Jesus' name, amen.",
  blog=None, video=None, plans=[]),

 dict(n=130, title="Out of the Depths", by="Anonymous",
  answer="Psalm 130 is a Song of Ascents and one of the church's seven penitential psalms. From the depths the psalmist cries to God, confessing that if God kept a record of sins no one could stand, but with Him there is forgiveness. Then the soul waits for the Lord more than watchmen wait for the morning.",
  body="""
<h2>What Psalm 130 means</h2>
<p>"Out of the depths I have cried to you, Yahweh." This is the deepest point of the climb, and it comes near the top. "If you, Yah, kept a record of sins, Lord, who could stand? But there is forgiveness with you, therefore you are feared."</p>
<p>Then comes the waiting: "My soul longs for the Lord more than watchmen long for the morning, more than watchmen for the morning." The repetition is the waiting itself. The night is long, but morning is certain.</p>
<p>The psalm ends with hope: "Israel, hope in Yahweh, for with Yahweh there is loving kindness. With him is abundant redemption."</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>Forgiveness opens the way into God's presence. The last line, "Israel, hope in Yahweh," is repeated in Psalm 131:3. Martin Luther turned this psalm into the hymn known in English as "Out of the Depths I Cry to You."</p>""",
  prompt="What are you waiting for, the way a night watchman waits for morning?",
  prayer="Lord, out of the depths I cry to You. Thank You that You do not keep a record of my sins, and that with You there is forgiveness. I will wait for You more than watchmen wait for the morning. In Jesus' name, amen.",
  blog=None, video=None, plans=[]),

 dict(n=131, title="A Quieted Soul", by="David",
  answer="Psalm 131 is a three-verse Song of Ascents by David about humility and rest in God. David says his heart is not proud and he does not chase things too great for him; instead he has calmed and quieted his soul like a weaned child with its mother. It teaches that stillness and humility are the ground of hope in God.",
  body="""
<h2>What Psalm 131 means</h2>
<p>"Yahweh, my heart isn't haughty, nor my eyes lofty; nor do I concern myself with great matters, or things too wonderful for me." David, a king with every reason to grasp for more, lays down the need to control what is beyond him.</p>
<p>"Surely I have stilled and quieted my soul, like a weaned child with his mother." The picture is precise. A nursing infant comes to its mother hungry and demanding. A weaned child no longer comes only to get something. It simply rests with her. That is a soul at peace with God: not empty of desire, but content to be with Him.</p>
<p>The psalm ends by turning outward: "Israel, hope in Yahweh, from this time forward and forever more."</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>After the long wait of Psalm 130 comes stillness. Humility and hope belong together, and this is the posture the whole climb has been forming. Stillness is not the absence of prayer. It is the ground of it.</p>""",
  prompt="What would it look like to come to God this week without asking for anything, just to be with Him?",
  prayer="Lord, I lay down the things too great for me. Quiet my soul like a weaned child resting with its mother. I don't come to get something. I come to be with You. My hope is in You, now and forever. In Jesus' name, amen.",
  blog="a-quieted-soul", video=V3, plans=[]),

 dict(n=132, title="A Dwelling Place", by="Anonymous",
  answer="Psalm 132 is the longest Song of Ascents and holds two oaths. David swears he will not rest until he finds a dwelling place for the Lord, and the Lord swears back that one of David's sons will sit on his throne forever. It holds David's longing for God's presence and God's greater promise, fulfilled in Jesus, the Son of David.",
  body="""
<h2>What Psalm 132 means</h2>
<p>In verses 1 to 10, David vows not to enter his house, go to bed or let his eyes sleep "until I find out a place for Yahweh, a dwelling for the Mighty One of Jacob." The people go to find the ark and cry, "Arise, Yahweh, into your resting place."</p>
<p>In verses 11 to 18, the Lord swears back to David: one of your sons will sit on your throne. "For Yahweh has chosen Zion. He has desired it for his habitation. 'This is my resting place forever.'"</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>This psalm picks up the house and sons of Psalm 127. "Arise, Yahweh" echoes Moses when the ark set out (Numbers 10:35) and Solomon's prayer at the dedication of the temple (2 Chronicles 6:41-42). It was likely sung in procession.</p>
<p>The promise to David finds its fulfillment in Jesus, the Son of David, and the dwelling place David longed to build is now a people: "you also are built together for a habitation of God in the Spirit" (Ephesians 2:22).</p>""",
  prompt="David would not rest until God had a place to dwell. What would it look like to make room for God's presence in your life?",
  prayer="Lord, I want my life to be a dwelling place for You. Give me David's hunger that would not rest until You had a home. Arise and fill Your church with Your presence. In Jesus' name, amen.",
  blog="a-dwelling-place-for-god", video=None, plans=[]),

 dict(n=133, title="How Good and Pleasant", by="David",
  answer="Psalm 133 is David's short Song of Ascents about unity. It says it is good and pleasant when God's people live together in unity, like precious oil poured on Aaron's head and like the dew of Mount Hermon falling on Zion, because there the Lord commands the blessing, life forevermore. It teaches that unity releases God's blessing.",
  body="""
<h2>What Psalm 133 means</h2>
<p>"See how good and how pleasant it is for brothers to live together in unity!" David gives two pictures.</p>
<p>First, unity is like the precious oil poured on Aaron's head when he was anointed as high priest, running down his beard and over the collar of his robes. It flows from the head downward and covers everything.</p>
<p>Second, it is like the dew of Hermon, the high mountain in the far north, falling on the hills of Zion. Fresh life from far away settling on dry ground.</p>
<p>Then the reason: "for there Yahweh gives the blessing, even life forever more."</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>In Psalm 122 the city was bound firmly together as the tribes went up. Here the people dwell together, and blessing flows from it. At the feast, families from every region camped side by side in Jerusalem. Unity was something you could see.</p>""",
  prompt="Where have you seen unity release blessing, and where is God asking you to pursue it?",
  prayer="Lord, make Your people one. Where there is division, pour out Your oil and Your dew. Show me where to pursue peace and unity, so that Your blessing would flow, life forevermore. In Jesus' name, amen.",
  blog="unity-releases-blessing", video=V4, plans=[]),

 dict(n=134, title="Hands Lifted in the Night", by="Anonymous",
  answer="Psalm 134 is the last Song of Ascents. It calls the servants of the Lord who stand by night in His house to lift their hands and bless the Lord, and it answers with a blessing from Zion. The climb that began in distress far from home ends in worship and blessing in the presence of God.",
  body="""
<h2>What Psalm 134 means</h2>
<p>"Look! Praise Yahweh, all you servants of Yahweh, who stand by night in Yahweh's house! Lift up your hands in the sanctuary. Praise Yahweh!"</p>
<p>Then the final word comes back: "May Yahweh bless you from Zion; even he who made heaven and earth." Many read this as the pilgrims calling to the priests on night watch, and the priests answering with a blessing.</p>

<h2>Where it fits in the Songs of Ascent</h2>
<p>This is the last step. "Yahweh's house" closes the bracket opened in Psalm 122:1. "He who made heaven and earth" appears for the third time (121:2 and 124:8). The climb ends the way the priestly blessing begins: the Lord bless you.</p>
<p>Worship at night, hands raised. "Let my prayer be set before you like incense; the lifting up of my hands like the evening sacrifice" (Psalm 141:2).</p>""",
  prompt="When was the last time you lifted your hands to bless the Lord, and what would make this week a night watch?",
  prayer="Lord, I lift my hands to bless You, even in the night. Thank You for bringing me all the way from far away into Your presence. Bless me from Zion, Maker of heaven and earth, and make my life a song of ascent. In Jesus' name, amen.",
  blog="unity-releases-blessing", video=V4, plans=[]),
]
