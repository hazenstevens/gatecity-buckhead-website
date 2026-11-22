# Spiritual Gifts Assessment data (Nov 22, 2026).
# Spec: Hazen approved a three-part gifts assessment on Nov 16, 2026 (Romans 12,
# 1 Corinthians 12, Ephesians 4). Snapshot on screen first (top two gifts), full
# results by email. Nov 18: each gift gets a static profile drawn from his books
# and teaching, which he reviews; only "how your gifts work together" is generated.
#
# One source of truth: build.py renders the page from PARTS/QUESTIONS, the SQL
# question map is generated from QUESTIONS, and the Mailchimp results email is
# generated from GIFTS (emails/gifts-results.html).

SERVE = "https://gatecity-buckhead.churchcenter.com/people/forms/856748"
PRAYER = "https://gatecitybuckhead.com/digital-community#prayer"
COHORT = "https://gatecitybuckhead.com/cohort"
VISIT = "https://gatecitybuckhead.com/new-here/"
GIVE = "https://gatecitybuckhead.com/pledge"

PARTS = [
    {"id": "r", "name": "Romans 12", "title": "Gifts of grace",
     "intro": "How God has wired you to love and serve. These are the everyday motivations Paul lists in Romans 12:6-8.",
     "verse": "Having gifts differing according to the grace that was given to us... let us use them.",
     "ref": "Romans 12:6"},
    {"id": "c", "name": "1 Corinthians 12", "title": "Gifts of the Spirit",
     "intro": "How the Holy Spirit shows up through you to help others. Answer from what you have experienced and what you find yourself hungry for. If some of these are new to you, that is okay. Paul says to earnestly desire them.",
     "verse": "But to each one is given the manifestation of the Spirit for the profit of all.",
     "ref": "1 Corinthians 12:7"},
    {"id": "e", "name": "Ephesians 4", "title": "Gifts that equip",
     "intro": "The five gifts Jesus gave to equip the church: apostle, prophet, evangelist, shepherd and teacher. We all function in these in degrees. This part shows which one you lean toward.",
     "verse": "He gave some to be apostles; and some, prophets; and some, evangelists; and some, shepherds and teachers; for the perfecting of the saints.",
     "ref": "Ephesians 4:11-12"},
]

# family: top two results never show two gifts from the same family
# kind: 1 Peter 4:10-11 sorts every gift into speaking or serving
GIFTS = {
  # ---------------- Romans 12 ----------------
  "r_prophecy": {
    "part": "r", "family": "prophetic", "kind": "speaking", "name": "Prophetic Perception",
    "ref": "Romans 12:6", "verse": "Having gifts differing according to the grace that was given to us: if prophecy, let us prophesy according to the proportion of our faith.",
    "teaser": "You tend to see what God is saying in a moment and feel compelled to say it.",
    "what": "In Romans 12, prophecy is a gift of grace that shapes how you see. You notice what God is doing and what He is saying, and you feel a strong pull to speak truth, call people back to God and stand for what is right.",
    "shows": ["You sense quickly when something is off spiritually or when God is moving.", "You care more about truth than comfort, and you want people to walk in it.", "You often pray before you speak, and your words land with weight."],
    "grow": ["Let love lead. Prophecy is for strengthening, encouraging and comforting people (1 Corinthians 14:3).", "Measure what you sense by Scripture and share it with gentle language.", "Pray more than you say. Many prophetic people do their best work in intercession."],
    "serve": "Join one of our prayer meetings, where seeing and praying go together.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you help people see what God is saying"},
  "r_serving": {
    "part": "r", "family": "serving", "kind": "serving", "name": "Serving",
    "ref": "Romans 12:7", "verse": "Or service, let us give ourselves to service.",
    "teaser": "You see the practical need and you love meeting it.",
    "what": "Serving is the grace to see a practical need and meet it with joy. People with this gift make the work of the church possible. It is the towel Jesus picked up in John 13, and it is never small in the Kingdom.",
    "shows": ["You notice what needs to be done before anyone asks.", "You find real joy in behind-the-scenes work.", "You would rather help than be thanked."],
    "grow": ["Serve from sonship, not for approval. You are already loved.", "Build rhythms of rest so serving stays a joy and not a burden.", "Invite someone to serve alongside you and pass on what you know."],
    "serve": "Our Sunday teams (welcome, kids, production and setup) are a great fit.", "link": SERVE, "link_text": "Join a serve team",
    "with": "you turn vision into practical help"},
  "r_teaching": {
    "part": "r", "family": "teaching", "kind": "speaking", "name": "Teaching",
    "ref": "Romans 12:7", "verse": "Or he who teaches, to his teaching.",
    "teaser": "You love to understand the Word and help others understand it too.",
    "what": "Teaching is the grace to understand God's truth and explain it so others can live it. Teachers slow us down and ask what the text actually says, then what it requires of us.",
    "shows": ["You love to dig into Scripture and context.", "People say you make hard things clear.", "You care about getting it right, not just getting it said."],
    "grow": ["Keep your own life in the Word before you teach others.", "Teach for obedience, not only information (James 1:22).", "Ask good questions. The best teachers help people discover."],
    "serve": "Help teach BuckCity Kids, or join Sunday Forum's Discovery Bible Study and help lead the conversation.", "link": SERVE, "link_text": "Serve as a teacher",
    "with": "you ground everything in the Word"},
  "r_encourage": {
    "part": "r", "family": "encourage", "kind": "speaking", "name": "Encouragement",
    "ref": "Romans 12:8", "verse": "Or he who exhorts, to his exhorting.",
    "teaser": "You call out the best in people and help them take the next step.",
    "what": "Encouragement, or exhortation, is the grace to come alongside people and strengthen them to keep going with God. The word Paul uses is close to the word Jesus used for the Holy Spirit, the One who comes alongside.",
    "shows": ["People seek you out when they need courage.", "You see potential in people before they see it themselves.", "You naturally think in next steps."],
    "grow": ["Keep your encouragement anchored in truth, not flattery.", "Write it down. A text or note can carry a word for years.", "Learn to listen well before you speak."],
    "serve": "Our welcome team and Digital Connect are where first-time guests meet encouragers.", "link": SERVE, "link_text": "Join the welcome team",
    "with": "you help people take the next step"},
  "r_giving": {
    "part": "r", "family": "giving", "kind": "serving", "name": "Giving",
    "ref": "Romans 12:8", "verse": "He who gives, let him do it with liberality.",
    "teaser": "You love to resource what God is doing, generously and gladly.",
    "what": "Giving is the grace to steward resources so God's work moves forward, and to do it with open hands. People with this gift often have a knack for creating resources and a joy in releasing them.",
    "shows": ["You light up when you can meet a need.", "You think about money, time and possessions as God's.", "You give quietly and you are glad to."],
    "grow": ["Give with simplicity and joy, not pressure (2 Corinthians 9:7).", "Ask God where He is moving and resource that.", "Pair generosity with wisdom and accountability."],
    "serve": "Partner with what God is doing in Buckhead through 99 for the 1.", "link": GIVE, "link_text": "Explore giving",
    "with": "you resource what God is doing"},
  "r_leading": {
    "part": "r", "family": "leading", "kind": "serving", "name": "Leadership",
    "ref": "Romans 12:8", "verse": "He who rules, with diligence.",
    "teaser": "You see where things need to go and help people get there together.",
    "what": "Leadership is the grace to set direction, organize people and carry responsibility with diligence. Godly leaders lead like Jesus, with a towel before the title.",
    "shows": ["People look to you when a group needs direction.", "You naturally organize and delegate.", "You feel responsible for the outcome and the people."],
    "grow": ["Lead from prayer. Direction comes from listening to God.", "Develop others, not just tasks.", "Stay accountable and teachable."],
    "serve": "Talk with us about leading a team or group, or step into the Discipleship Cohort.", "link": COHORT, "link_text": "Explore the Cohort",
    "with": "you bring direction and order"},
  "r_mercy": {
    "part": "r", "family": "mercy", "kind": "serving", "name": "Mercy",
    "ref": "Romans 12:8", "verse": "He who shows mercy, with cheerfulness.",
    "teaser": "You feel what hurting people feel and move toward them.",
    "what": "Mercy is the grace to feel compassion for people who are hurting and to move toward them with the kindness of Jesus. Mercy carries people through hard seasons.",
    "shows": ["You notice who is left out or hurting.", "You are drawn to people in pain, not away from them.", "Your presence brings comfort."],
    "grow": ["Let God carry what you carry. Bring people to Him in prayer.", "Set healthy boundaries so compassion stays cheerful.", "Pair mercy with the hope of the gospel."],
    "serve": "Join a prayer meeting or ask about caring for people during Sunday Ministry Time.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you carry people with compassion"},
  # ---------------- 1 Corinthians 12 ----------------
  "c_wisdom": {
    "part": "c", "family": "wisdom", "kind": "speaking", "name": "Word of Wisdom",
    "ref": "1 Corinthians 12:8", "verse": "For to one is given through the Spirit the word of wisdom.",
    "teaser": "The Spirit gives you insight into what to do next.",
    "what": "A word of wisdom is revelation about the future or God's wisdom for what to do next. Agabus foretold a famine and the church sent relief ahead of time (Acts 11:28-30). Philip was told to go to the desert road (Acts 8:26).",
    "shows": ["You get a sense of direction for a decision that turns out right.", "People ask you, \"What should I do?\"", "You sense timely warnings or next steps in prayer."],
    "grow": ["Ask, \"Holy Spirit, what are You doing?\" (John 5:19).", "Write down what you sense and watch how God confirms it.", "Offer wisdom humbly and let people weigh it."],
    "serve": "Pray with people after services and in our prayer meetings.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you sense the next step"},
  "c_knowledge": {
    "part": "c", "family": "knowledge", "kind": "speaking", "name": "Word of Knowledge",
    "ref": "1 Corinthians 12:8", "verse": "And to another the word of knowledge, according to the same Spirit.",
    "teaser": "The Spirit shows you things you could not have known, to help people meet God.",
    "what": "A word of knowledge is a piece of information the Spirit reveals about the past or present that you could not have known naturally. It is a fragment, not the whole picture. Jesus told the woman at the well about her five husbands, and one sentence opened her heart (John 4:18).",
    "shows": ["As you pray, a name, a body part or a situation comes to mind.", "You get impressions that turn out to be specific and true.", "You gently ask, \"Does this mean anything to you?\""],
    "grow": ["Value small impressions. One can be the key that opens a door.", "Use gentle language. If you miss it, no one gets hurt.", "Don't fear missing it. The bigger risk is never stepping out."],
    "serve": "Pray for people in our prayer meetings and after services.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you hear what the Spirit is highlighting"},
  "c_faith": {
    "part": "c", "family": "faith", "kind": "serving", "name": "Faith",
    "ref": "1 Corinthians 12:9", "verse": "To another faith, by the same Spirit.",
    "teaser": "You carry a settled confidence that God will act.",
    "what": "The gift of faith is a supernatural confidence that God will act, often bringing protection, provision or direction you could not have arranged. Daniel in the lions' den, Elijah fed by ravens and Paul in the storm all carried it.",
    "shows": ["In a crisis, you feel a deep, settled certainty.", "You pray bold prayers and expect answers.", "Your faith stirs faith in others."],
    "grow": ["Feed your faith on the Word (Romans 10:17).", "Keep a record of answered prayer.", "Stand with others who need faith in hard seasons."],
    "serve": "Our night and day prayer rhythm needs people who believe God will answer.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you believe God will move"},
  "c_healing": {
    "part": "c", "family": "healing", "kind": "serving", "name": "Gifts of Healing",
    "ref": "1 Corinthians 12:9", "verse": "And to another gifts of healings, by the same Spirit.",
    "teaser": "You are drawn to pray for the sick and expect God to touch them.",
    "what": "In the Greek, both gifts and healings are plural. Healing comes in many forms and often unfolds as a process. Jesus healed in different ways, and He has not stopped.",
    "shows": ["You feel compassion and boldness to pray when someone is sick.", "You have seen people improve after prayer.", "You find yourself asking, \"How do you feel now?\""],
    "grow": ["Lay a hand on a shoulder, pray simply, and ask how they feel.", "Thank God for every bit of improvement. Value small measures.", "Keep praying. Healing is often a process."],
    "serve": "Ask about praying for people during Sunday Ministry Time.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you bring the healing touch of Jesus"},
  "c_miracles": {
    "part": "c", "family": "miracles", "kind": "serving", "name": "Working of Miracles",
    "ref": "1 Corinthians 12:10", "verse": "And to another workings of miracles.",
    "teaser": "You expect God to change the circumstances themselves.",
    "what": "A miracle is a supernatural intervention in the ordinary course of nature, usually instant. The gift of faith kept Paul safe in the storm. The working of miracles is Jesus rebuking the storm so it stopped.",
    "shows": ["You are drawn to pray for situations that seem impossible.", "You have seen God change circumstances beyond natural explanation.", "You are not easily intimidated by hard situations."],
    "grow": ["Stay close to Jesus. Miracles flow from relationship, not technique.", "Pray with others; the gifts rarely work alone.", "Give God the glory, every time it happens."],
    "serve": "Join our prayer meetings and pray for the city and the nations.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you expect God to intervene"},
  "c_prophecy": {
    "part": "c", "family": "prophetic", "kind": "speaking", "name": "Prophecy",
    "ref": "1 Corinthians 12:10", "verse": "But he who prophesies speaks to men for their edification, exhortation, and consolation. (1 Corinthians 14:3)",
    "teaser": "The Spirit gives you words that strengthen, encourage and comfort.",
    "what": "Prophecy is speaking a message from God to strengthen, encourage and comfort people. Paul tells us to earnestly desire it because it builds up the church, and he says everyone can prophesy (1 Corinthians 14:1, 31).",
    "shows": ["An encouraging word, a picture or a Scripture comes to mind for someone.", "Your words land exactly where people are.", "You sense God's heart for people."],
    "grow": ["Earnestly desire it, and start in small ways.", "Don't force it. Stay open to the Spirit.", "Submit words to Scripture and to trusted leaders."],
    "serve": "Pray for people in our prayer meetings and during Ministry Time.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you speak words that build people up"},
  "c_discern": {
    "part": "c", "family": "discern", "kind": "speaking", "name": "Discerning of Spirits",
    "ref": "1 Corinthians 12:10", "verse": "And to another discerning of spirits.",
    "teaser": "You perceive what is really at work beneath the surface.",
    "what": "Discerning of spirits is insight into the spiritual realm: perceiving whether what is at work is the Holy Spirit, a human spirit or an evil spirit. It is more than reading people. Paul discerned the spirit behind the slave girl in Philippi and set her free (Acts 16:16-18).",
    "shows": ["You sense the spiritual atmosphere of a room.", "You can tell when something sounds right but is not of God.", "You know how to pray because you see what is going on."],
    "grow": ["Let discernment lead you to prayer, not suspicion.", "Grow in the Word so you can test what you sense.", "Stay humble and share what you see with care."],
    "serve": "Our intercessors need discerning people.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you see what is really going on"},
  "c_tongues": {
    "part": "c", "family": "tongues", "kind": "speaking", "name": "Tongues",
    "ref": "1 Corinthians 12:10", "verse": "He who speaks in another language edifies himself. (1 Corinthians 14:4)",
    "teaser": "You pray in the Spirit, and it builds you up.",
    "what": "Tongues is speaking in a language you have not learned, whether a human language or the tongues of angels. A private prayer language builds you up (1 Corinthians 14:2-4). A message in tongues for the church should be interpreted.",
    "shows": ["You pray in tongues, or you are hungry to.", "Praying in the Spirit strengthens your walk with God.", "You sense times to pray when words run out."],
    "grow": ["Pray in the Spirit daily, even for a few minutes.", "Ask for interpretation (1 Corinthians 14:13).", "Read How to Be Filled With the Holy Spirit."],
    "serve": "Join our prayer meetings and pray in the Spirit with others.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you pray in the Spirit"},
  "c_interp": {
    "part": "c", "family": "interp", "kind": "speaking", "name": "Interpretation of Tongues",
    "ref": "1 Corinthians 12:10", "verse": "And to another the interpretation of languages.",
    "teaser": "You help people understand what the Spirit is saying.",
    "what": "Interpretation is the Spirit-given ability to express the meaning of a message in tongues. It is more than translating words. It conveys God's heart and burden so the whole church is built up.",
    "shows": ["When you hear tongues, a sense of meaning rises in you.", "You are drawn to make spiritual things understandable.", "Your words bring encouragement after a message."],
    "grow": ["Pray for the gift of interpretation as you pray in tongues.", "Share what you sense humbly and let it be weighed.", "Stay in the Word so you know God's heart."],
    "serve": "Prayer meetings are a safe place to grow in this gift.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you make the Spirit's voice understandable"},
  # ---------------- Ephesians 4 ----------------
  "e_apostle": {
    "part": "e", "family": "apostle", "kind": "serving", "name": "Apostle (Pioneer)",
    "ref": "Ephesians 4:11", "verse": "He gave some to be apostles... for the perfecting of the saints, to the work of serving, to the building up of the body of Christ.",
    "teaser": "You are a pioneer. You want to build new things and establish order.",
    "what": "The apostolic gift is about pioneering and establishing order. Apostolic people take new ground, see the bigger picture and build. Most of us will not carry the office, but many of us carry this grace in degrees.",
    "shows": ["You dream about starting new things for God.", "You see how pieces fit into a bigger plan.", "You raise up others and then move on to the next thing."],
    "grow": ["The towel before the title. The greater the grace, the lower the posture.", "Build according to what God is saying, with prophetic people near you.", "Let your community affirm your calling over time."],
    "serve": "Talk with us about pioneering a group or outreach, and step into the Discipleship Cohort.", "link": COHORT, "link_text": "Explore the Cohort",
    "with": "you pioneer new ground"},
  "e_prophet": {
    "part": "e", "family": "prophetic", "kind": "speaking", "name": "Prophet",
    "ref": "Ephesians 4:11", "verse": "And some, prophets.",
    "teaser": "You carry God's vision and help others hear His voice.",
    "what": "Prophets understand, see and hear the vision of God. They provide the blueprint the apostolic builds by. Haggai and Zechariah did not lay the stones, but the builders rose up when the word of the Lord came (Ezra 5:1-2).",
    "shows": ["You sense God's vision for people, places or the church.", "You are drawn to intercession.", "You stir others to hear God for themselves."],
    "grow": ["Equip others to hear God; don't just hear for them.", "Stay accountable and submit words to leaders.", "Pray as much as you speak."],
    "serve": "Our night and day prayer rhythm is where prophetic people thrive.", "link": PRAYER, "link_text": "Join a prayer meeting",
    "with": "you carry God's vision"},
  "e_evangelist": {
    "part": "e", "family": "evangelist", "kind": "speaking", "name": "Evangelist",
    "ref": "Ephesians 4:11", "verse": "And some, evangelists.",
    "teaser": "Your heart beats for people to know Jesus.",
    "what": "The evangelist's relentless focus is that people would be born again. All of us are called to be witnesses, but some carry a particular grace both to win people and to train others to share their faith.",
    "shows": ["You think about people who don't know Jesus.", "Sharing your faith feels natural, even exciting.", "You stir others to share the gospel."],
    "grow": ["Pray by name for people who don't yet know Jesus.", "Keep your story fresh. Share what Jesus is doing now.", "Bring someone with you. Train as you go."],
    "serve": "Invite your one to church, and help us at outreach events in Buckhead.", "link": VISIT, "link_text": "Invite someone Sunday",
    "with": "you bring people to Jesus"},
  "e_shepherd": {
    "part": "e", "family": "shepherd", "kind": "serving", "name": "Shepherd",
    "ref": "Ephesians 4:11", "verse": "And some, shepherds and teachers.",
    "teaser": "You care deeply about how people are doing and help them grow.",
    "what": "Shepherds care about the spiritual health of people. They notice, show up and keep walking with people, not just in crisis but in the slow work of formation. They strengthen the body so it can endure.",
    "shows": ["You notice when someone is struggling.", "You love walking with people over time.", "People open up to you."],
    "grow": ["Care from Christ's love, not your own strength.", "Train others to care; you can't carry everyone.", "Keep your own soul healthy."],
    "serve": "Help lead a group, or step into the Discipleship Cohort and walk with others.", "link": COHORT, "link_text": "Explore the Cohort",
    "with": "you care for people over the long haul"},
  "e_teacher": {
    "part": "e", "family": "teaching", "kind": "speaking", "name": "Teacher",
    "ref": "Ephesians 4:11", "verse": "And some, shepherds and teachers; for the perfecting of the saints.",
    "teaser": "You equip others to handle the Word for themselves.",
    "what": "Teachers in Ephesians 4 are concerned with what God has said through the Scriptures: sound doctrine and practical obedience. They equip the whole body to study, handle Scripture rightly and disciple one another.",
    "shows": ["You want people to understand the Bible for themselves.", "You notice when teaching drifts from the text.", "You love helping others teach."],
    "grow": ["Equip, don't just explain. Help others learn to study.", "Stay a learner yourself.", "Pair truth with love."],
    "serve": "Help lead Discovery Bible Study at Sunday Forum or a Formation Night conversation.", "link": SERVE, "link_text": "Serve as a teacher",
    "with": "you equip others in the Word"},
}

# Questions: 3 per Romans 12 and Ephesians 4 gift, 2 per 1 Corinthians 12 gift (54 total).
QUESTIONS = [
  # Romans 12
  ("r1", "r_prophecy", "I quickly sense when something is spiritually off, or when God is moving."),
  ("r2", "r_prophecy", "I feel compelled to speak up for truth, even when it isn't popular."),
  ("r3", "r_prophecy", "I often sense what God wants to say to a person or a situation."),
  ("r4", "r_serving", "I notice practical needs and meet them before anyone asks."),
  ("r5", "r_serving", "I find real joy in behind-the-scenes work."),
  ("r6", "r_serving", "I would rather help with a task than lead it."),
  ("r7", "r_teaching", "I love studying the Bible to understand what it really says."),
  ("r8", "r_teaching", "People tell me I explain things clearly."),
  ("r9", "r_teaching", "I get energized when I help someone understand a truth from Scripture."),
  ("r10", "r_encourage", "People come to me when they need courage to keep going."),
  ("r11", "r_encourage", "I see potential in people and enjoy calling it out."),
  ("r12", "r_encourage", "I naturally help people find their next step."),
  ("r13", "r_giving", "I find deep joy in giving to meet a need."),
  ("r14", "r_giving", "I look for ways to use my resources for God's work."),
  ("r15", "r_giving", "I give generously and gladly, even when no one knows."),
  ("r16", "r_leading", "When a group lacks direction, I tend to step in and organize it."),
  ("r17", "r_leading", "I can see where a team needs to go and help people get there."),
  ("r18", "r_leading", "I enjoy carrying responsibility for people and outcomes."),
  ("r19", "r_mercy", "I feel deep compassion for people who are hurting."),
  ("r20", "r_mercy", "I notice who is left out and move toward them."),
  ("r21", "r_mercy", "I'm glad to spend time with people in hard seasons."),
  # 1 Corinthians 12
  ("c1", "c_wisdom", "I've had moments when God gave me clear direction for what someone should do next."),
  ("c2", "c_wisdom", "People ask me for wisdom in decisions, and it often proves right."),
  ("c3", "c_knowledge", "While praying for someone, I've sensed specific details I couldn't have known."),
  ("c4", "c_knowledge", "I find myself hungry to hear specific things from the Holy Spirit for others."),
  ("c5", "c_faith", "In a crisis, I often feel a settled confidence that God will act."),
  ("c6", "c_faith", "I pray bold prayers and expect God to answer."),
  ("c7", "c_healing", "I feel compassion and boldness to pray for people who are sick."),
  ("c8", "c_healing", "I've seen people improve or be healed after I prayed for them."),
  ("c9", "c_miracles", "I'm drawn to pray for situations that seem impossible."),
  ("c10", "c_miracles", "I've seen God change circumstances in ways that had no natural explanation."),
  ("c11", "c_prophecy", "Encouraging words, pictures or Scriptures come to mind for people as I pray."),
  ("c12", "c_prophecy", "When I share what I sense from God, people tell me it strengthened them."),
  ("c13", "c_discern", "I can sense the spiritual atmosphere of a room or situation."),
  ("c14", "c_discern", "I can tell when something sounds right but isn't from God."),
  ("c15", "c_tongues", "I pray in tongues, or I'm hungry to receive a prayer language."),
  ("c16", "c_tongues", "Praying in the Spirit builds me up and strengthens my walk with God."),
  ("c17", "c_interp", "When I hear a message in tongues, I sense what it means."),
  ("c18", "c_interp", "I'm drawn to help people understand what the Spirit is saying."),
  # Ephesians 4
  ("e1", "e_apostle", "I dream about starting new things for God: groups, ministries or churches."),
  ("e2", "e_apostle", "I see how the pieces fit into a bigger plan and enjoy building it."),
  ("e3", "e_apostle", "I enjoy raising up others so a work can continue without me."),
  ("e4", "e_prophet", "I sense God's vision for people, places or the church."),
  ("e5", "e_prophet", "I'm drawn to long seasons of intercession."),
  ("e6", "e_prophet", "I love helping others learn to hear God's voice."),
  ("e7", "e_evangelist", "I think often about people who don't know Jesus."),
  ("e8", "e_evangelist", "Sharing my faith feels natural, even exciting."),
  ("e9", "e_evangelist", "I enjoy equipping others to share the gospel."),
  ("e10", "e_shepherd", "I notice when someone is struggling and check in."),
  ("e11", "e_shepherd", "I love walking with people over the long haul."),
  ("e12", "e_shepherd", "People open up to me about their spiritual lives."),
  ("e13", "e_teacher", "I want people to be able to study the Bible for themselves."),
  ("e14", "e_teacher", "I notice when teaching drifts from what Scripture says."),
  ("e15", "e_teacher", "I enjoy helping others become better teachers of the Word."),
]

SYNERGY_TAIL = {
    ("speaking", "speaking"): "Both are speaking gifts (1 Peter 4:11), so watch for chances to put words into action alongside others.",
    ("serving", "serving"): "Both are serving gifts (1 Peter 4:11), so you may build up the church most through what you do, and your words will carry that weight.",
    ("mixed",): "One is a speaking gift and one a serving gift (1 Peter 4:11), a strong pair: you can both say it and live it.",
}


def synergy(g1, g2):
    a, b = GIFTS[g1], GIFTS[g2]
    k = (a["kind"], b["kind"]) if a["kind"] == b["kind"] else ("mixed",)
    s = "With %s, %s. With %s, %s. %s" % (a["name"], a["with"], b["name"], b["with"], SYNERGY_TAIL[k])
    return s
