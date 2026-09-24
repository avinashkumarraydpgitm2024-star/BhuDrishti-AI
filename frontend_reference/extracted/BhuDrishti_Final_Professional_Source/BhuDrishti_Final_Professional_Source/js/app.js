
(function(){
'use strict';
const LANG_KEY='bhudrishtiLanguage',THEME_KEY='bhudrishtiTheme',AREA_KEY='bhudrishtiCurrentArea',READ_KEY='bhudrishtiReadAlerts';
const T={
 en:{
  main:'MAIN',tools:'TOOLS',account:'ACCOUNT',home:'Home',map:'Map',alerts:'Alerts',assistant:'AI Assistant',safety:'Area Safety',change:'Change Detection',saved:'Saved Places',settings:'Settings',help:'Help & Support',
  yourArea:'Your area',welcome:'Welcome',logout:'Log out',profileMenuSettings:'Settings',profileMenuSaved:'Saved places',
  homeEyebrow:"TODAY'S AREA UPDATE",homeTitle:'Good morning,',homeDesc:'A clear snapshot of safety around your selected area.',viewSafety:'View area safety',openMap:'Open map',currentRisk:'Current risk',primaryRisk:'Primary risk',whyRisk:'Why this risk?',weather:'Weather',weatherText:'Comfortable conditions right now',rain:'Rain',wind:'Wind',humidity:'Humidity',researchPreview:'Research-based safety preview.',researchMarkers:'30 researched locations with clear risk markers.',changeCardText:'Compare older and newer images in a simple flow.',savedCardText:'Keep important places one tap away.',
  safetyHero:'Know the risk before you move.',safetyDesc:'Pick a researched location and get a clear safety view: risk, reason, warning signs, safer timing and route guidance.',researchLocations:'30 verified locations · available offline',checkLocation:'Check a location',searchResearch:'Search the 30 verified Sikkim research cases',checkSafety:'Check safety',locationNotFound:'No matching researched location found. Try a place from the suggestions.',riskScore:'research risk score',warningSigns:'Warning signs',safetySteps:'Safety steps',riskReduction:'When risk may reduce',safeRoute:'Safer place / route',officialSource:'Verified research source',openSource:'Open official source',datasetNote:'This is a research-based prototype score, not a live government warning. Always follow current official alerts.',mapOpen:'Open map',
  mapHero:'See risk around you.',mapDesc:'Explore researched locations, filter by risk level and open safety details in one tap.',allLocations:'All locations',highRisk:'High risk',mediumRisk:'Medium risk',lowRisk:'Low risk',selectedLocation:'Selected location',viewDetails:'View details',selectMarker:'Select a marker',verifiedLocations:'30 verified research locations',
  alertsHero:'Only the alerts that matter.',alertsDesc:'Important warnings and safety reminders, kept simple and readable.',markRead:'Mark all as read',unreadAlerts:'unread alerts',allCaughtUp:'You are all caught up',markThisRead:'Mark as read',read:'Read',
  alert1Title:'Heavy rainfall watch',alert1Body:'Some landslide-prone roads may become unstable if rain continues.',alert1Time:'12 min ago',alert2Title:'Road caution',alert2Body:'Use only officially opened routes near steep slopes.',alert2Time:'38 min ago',alert3Title:'Daily safety tip',alert3Body:'Keep emergency numbers and one offline map screenshot ready.',alert3Time:'2 hr ago',alert4Title:'Teesta corridor reminder',alert4Body:'Avoid low-lying riverbank areas during official flood warnings.',alert4Time:'5 hr ago',
  aiHero:'Ask about safety in simple language.',aiDesc:'An offline demo assistant for common risk, travel and emergency questions.',typeQuestion:'Type your question…',send:'Send',quick1:'Is this landslide area safe?',quick2:'What should I do in a flood?',quick3:'How do I find a safer route?',aiGreeting:'Hi! Ask me about local risk, safer routes, flood or landslide precautions.',aiFlood:'Move away from riverbanks and low-lying areas, never cross floodwater, and follow official alerts. Open Area Safety for location-specific guidance.',aiLandslide:'During heavy rain, avoid steep or unstable slopes and roads with fresh debris or cracks. Use only routes officially reopened by authorities.',aiRoute:'Open Area Safety for the selected location, then use the safer route guidance and Map button. Routes should always be confirmed by current local advisories.',aiEmergency:'If there is an immediate danger, move to a safer open or higher area and follow local emergency instructions. Do not enter blocked roads or active hazard zones.',aiFallback:'I can help with flood, landslide, road safety, safer routes and BhuDrishti features. Try asking one of those topics.',
  changeHero:'See what changed, clearly.',changeDesc:'Compare an older and newer image and get a simple change summary without a technical dashboard.',olderImage:'Older image',newerImage:'Newer image',chooseImage:'Choose image',compare:'Compare images',trySample:'Try sample',changeSummary:'Change summary',possibleImpact:'Possible impact',suggestedAction:'Suggested action',changePercent:'Change detected',noImages:'Add both images to compare.',samplePrompt:'Upload images or try the sample first.',sampleSummary:'Visible surface and land-cover change detected in the sample pair.',sampleImpact:'Changes near roads, slopes or water channels may need a closer safety review.',sampleAction:'Review the changed zone and compare it with current weather and local risk information.',
  savedHero:'Keep important places one tap away.',savedDesc:'Save locations you care about and open their safety details quickly.',addPlace:'Save place',searchPlaces:'Search a location',noSaved:'No saved places yet. Search a researched location above and save it.',remove:'Remove',
  settingsHero:'Make BhuDrishti work your way.',settingsDesc:'Choose language, theme and simple notification preferences.',appearance:'Appearance',appearanceDesc:'Choose a comfortable theme.',language:'Language',languageDesc:'English, Hindi or Hinglish across the full interface.',light:'Light',dark:'Dark',profile:'Profile',displayName:'Display name',save:'Save changes',notifications:'Notifications',riskAlerts:'Risk alerts',riskAlertsDesc:'Show important location-risk notifications.',weatherAlerts:'Weather alerts',weatherAlertsDesc:'Show weather-related safety notifications.',data:'DATA',offlinePrototype:'Offline prototype',offlineDesc:'Research data and demo preferences stay in this browser. No server is required for the prototype.',
  helpHero:'Help, without the hassle.',helpDesc:'Quick answers for using the prototype.',faq1Q:'How do I check risk?',faq1A:'Open Area Safety, choose one of the 30 researched locations and press Check safety.',faq2Q:'Does this need internet?',faq2A:'The main prototype works offline. Internet is only needed to open external official source pages.',faq3Q:'Why is the risk score not live?',faq3A:'It is a research-based project score. A production version would combine live weather, sensors and authority alerts.',faq4Q:'Where is my data stored?',faq4A:'Demo preferences and saved places are stored locally in your browser.',
  loginVisualTitle:'Local safety, made simple.',loginVisualDesc:'Risk details, map guidance, alerts and change detection in one calm user experience.',loginFoot:'Offline-ready prototype · 30 researched locations',loginTitle:'Welcome back',loginSub:'Sign in to continue to your safety dashboard.',email:'Email',password:'Password',login:'Sign in',demo:'Use demo account',loginError:'Enter a valid email and at least 4 characters for password.',
  verifyVisualTitle:'One quick check. Then you’re in.',verifyVisualDesc:'A clean demo verification step that works fully offline.',verifyFoot:'No network request is required',verifyTitle:'Verify your account',verifySub:'Enter the 6-digit demo code sent to',verify:'Verify & continue',resend:'Resend code',verifyNote:'For this offline prototype, use code 123456.',verifyError:'Enter the 6-digit demo code 123456.',resendDone:'Demo code is 123456.',
  sourceNotePrefix:'Official SSDMA research reference',high:'High',medium:'Medium',low:'Low',risk:'risk',district:'District',
 },
 hi:{
  main:'मुख्य',tools:'टूल्स',account:'अकाउंट',home:'होम',map:'मैप',alerts:'अलर्ट',assistant:'AI सहायक',safety:'एरिया सेफ्टी',change:'बदलाव पहचान',saved:'सेव की गई जगहें',settings:'सेटिंग्स',help:'मदद और सपोर्ट',
  yourArea:'आपका क्षेत्र',welcome:'स्वागत',logout:'लॉग आउट',profileMenuSettings:'सेटिंग्स',profileMenuSaved:'सेव की गई जगहें',
  homeEyebrow:'आज का एरिया अपडेट',homeTitle:'सुप्रभात,',homeDesc:'आपके चुने हुए क्षेत्र की सुरक्षा स्थिति एक साफ और आसान रूप में।',viewSafety:'एरिया सेफ्टी देखें',openMap:'मैप खोलें',currentRisk:'वर्तमान जोखिम',primaryRisk:'मुख्य जोखिम',whyRisk:'जोखिम क्यों है?',weather:'मौसम',weatherText:'अभी मौसम सामान्य और आरामदायक है',rain:'बारिश',wind:'हवा',humidity:'नमी',researchPreview:'रिसर्च पर आधारित सुरक्षा सारांश।',researchMarkers:'30 रिसर्च लोकेशन साफ जोखिम मार्कर के साथ।',changeCardText:'पुरानी और नई तस्वीर की आसान तुलना करें।',savedCardText:'जरूरी जगहें एक टैप में खोलें।',
  safetyHero:'आगे बढ़ने से पहले जोखिम जानें।',safetyDesc:'रिसर्च की गई जगह चुनें और जोखिम, कारण, चेतावनी संकेत, सुरक्षित समय और मार्ग की साफ जानकारी देखें।',researchLocations:'30 सत्यापित लोकेशन · ऑफलाइन उपलब्ध',checkLocation:'जगह की सुरक्षा देखें',searchResearch:'सिक्किम के 30 सत्यापित रिसर्च केस में खोजें',checkSafety:'सुरक्षा देखें',locationNotFound:'मिलती हुई रिसर्च लोकेशन नहीं मिली। ऊपर दिए सुझावों में से जगह चुनें।',riskScore:'रिसर्च जोखिम स्कोर',warningSigns:'चेतावनी के संकेत',safetySteps:'सुरक्षा के कदम',riskReduction:'जोखिम कब कम हो सकता है',safeRoute:'सुरक्षित जगह / मार्ग',officialSource:'सत्यापित रिसर्च स्रोत',openSource:'आधिकारिक स्रोत खोलें',datasetNote:'यह रिसर्च पर आधारित प्रोटोटाइप स्कोर है, लाइव सरकारी चेतावनी नहीं। हमेशा वर्तमान आधिकारिक अलर्ट मानें।',mapOpen:'मैप खोलें',
  mapHero:'अपने आसपास का जोखिम देखें।',mapDesc:'रिसर्च लोकेशन देखें, जोखिम स्तर से फ़िल्टर करें और एक टैप में सुरक्षा विवरण खोलें।',allLocations:'सभी लोकेशन',highRisk:'उच्च जोखिम',mediumRisk:'मध्यम जोखिम',lowRisk:'कम जोखिम',selectedLocation:'चुनी गई जगह',viewDetails:'विवरण देखें',selectMarker:'मार्कर चुनें',verifiedLocations:'30 सत्यापित रिसर्च लोकेशन',
  alertsHero:'सिर्फ जरूरी अलर्ट।',alertsDesc:'महत्वपूर्ण चेतावनी और सुरक्षा रिमाइंडर, बिना अनावश्यक जानकारी के।',markRead:'सभी को पढ़ा हुआ करें',unreadAlerts:'अपठित अलर्ट',allCaughtUp:'सभी अलर्ट पढ़े जा चुके हैं',markThisRead:'पढ़ा हुआ करें',read:'पढ़ा हुआ',
  alert1Title:'भारी बारिश की निगरानी',alert1Body:'बारिश जारी रहने पर भूस्खलन वाले कुछ सड़क क्षेत्र अस्थिर हो सकते हैं।',alert1Time:'12 मिनट पहले',alert2Title:'सड़क सावधानी',alert2Body:'खड़ी ढलानों के पास केवल आधिकारिक रूप से खुले मार्ग का उपयोग करें।',alert2Time:'38 मिनट पहले',alert3Title:'आज की सुरक्षा टिप',alert3Body:'आपात नंबर और एक ऑफलाइन मैप स्क्रीनशॉट तैयार रखें।',alert3Time:'2 घंटे पहले',alert4Title:'तीस्ता कॉरिडोर याद दिलाना',alert4Body:'आधिकारिक बाढ़ चेतावनी के दौरान निचले नदी किनारे वाले क्षेत्रों से दूर रहें।',alert4Time:'5 घंटे पहले',
  aiHero:'सुरक्षा के बारे में आसान भाषा में पूछें।',aiDesc:'आम जोखिम, यात्रा और आपात सवालों के लिए ऑफलाइन डेमो सहायक।',typeQuestion:'अपना सवाल लिखें…',send:'भेजें',quick1:'क्या यह भूस्खलन क्षेत्र सुरक्षित है?',quick2:'बाढ़ में मुझे क्या करना चाहिए?',quick3:'सुरक्षित मार्ग कैसे देखें?',aiGreeting:'नमस्ते! स्थानीय जोखिम, सुरक्षित मार्ग, बाढ़ या भूस्खलन सुरक्षा के बारे में पूछें।',aiFlood:'नदी किनारे और निचले क्षेत्रों से दूर जाएँ, बाढ़ के पानी को पार न करें और आधिकारिक अलर्ट मानें। जगह के अनुसार जानकारी के लिए एरिया सेफ्टी खोलें।',aiLandslide:'भारी बारिश में खड़ी या अस्थिर ढलानों और ताजा मलबे या दरार वाली सड़कों से दूर रहें। केवल आधिकारिक रूप से दोबारा खोले गए मार्ग का उपयोग करें।',aiRoute:'चुनी गई जगह के लिए एरिया सेफ्टी खोलें, फिर सुरक्षित मार्ग की जानकारी और मैप बटन देखें। मार्ग हमेशा वर्तमान स्थानीय सलाह से सत्यापित करें।',aiEmergency:'तुरंत खतरा हो तो सुरक्षित खुले या ऊँचे स्थान पर जाएँ और स्थानीय आपात निर्देश मानें। बंद सड़क या सक्रिय खतरे वाले क्षेत्र में न जाएँ।',aiFallback:'मैं बाढ़, भूस्खलन, सड़क सुरक्षा, सुरक्षित मार्ग और BhuDrishti फीचर में मदद कर सकता हूँ। इनमें से कोई विषय पूछें।',
  changeHero:'साफ तरीके से देखें क्या बदला।',changeDesc:'पुरानी और नई तस्वीर की तुलना करें और बिना तकनीकी डैशबोर्ड के आसान बदलाव सारांश देखें।',olderImage:'पुरानी तस्वीर',newerImage:'नई तस्वीर',chooseImage:'तस्वीर चुनें',compare:'तस्वीरें तुलना करें',trySample:'सैंपल देखें',changeSummary:'बदलाव सारांश',possibleImpact:'संभावित असर',suggestedAction:'सुझाया गया कदम',changePercent:'पता चला बदलाव',noImages:'तुलना के लिए दोनों तस्वीरें जोड़ें।',samplePrompt:'तस्वीरें अपलोड करें या पहले सैंपल देखें।',sampleSummary:'सैंपल जोड़ी में सतह और भूमि आवरण में साफ बदलाव दिखा।',sampleImpact:'सड़क, ढलान या जलमार्ग के पास बदलाव हो तो सुरक्षा की अतिरिक्त जांच जरूरी हो सकती है।',sampleAction:'बदले हुए क्षेत्र की समीक्षा करें और उसे वर्तमान मौसम तथा स्थानीय जोखिम जानकारी से मिलाएँ।',
  savedHero:'जरूरी जगहें एक टैप की दूरी पर रखें।',savedDesc:'अपनी महत्वपूर्ण लोकेशन सेव करें और उनकी सुरक्षा जानकारी जल्दी खोलें।',addPlace:'जगह सेव करें',searchPlaces:'लोकेशन खोजें',noSaved:'अभी कोई जगह सेव नहीं है। ऊपर रिसर्च लोकेशन खोजकर सेव करें।',remove:'हटाएँ',
  settingsHero:'BhuDrishti को अपने हिसाब से सेट करें।',settingsDesc:'भाषा, थीम और आसान नोटिफिकेशन प्राथमिकताएँ चुनें।',appearance:'दिखावट',appearanceDesc:'आरामदायक थीम चुनें।',language:'भाषा',languageDesc:'पूरे इंटरफेस में English, हिंदी या Hinglish चुनें।',light:'लाइट',dark:'डार्क',profile:'प्रोफाइल',displayName:'दिखने वाला नाम',save:'बदलाव सेव करें',notifications:'नोटिफिकेशन',riskAlerts:'रिस्क अलर्ट',riskAlertsDesc:'महत्वपूर्ण लोकेशन रिस्क नोटिफिकेशन दिखाएँ।',weatherAlerts:'मौसम अलर्ट',weatherAlertsDesc:'मौसम से जुड़े सुरक्षा नोटिफिकेशन दिखाएँ।',data:'डेटा',offlinePrototype:'ऑफलाइन प्रोटोटाइप',offlineDesc:'रिसर्च डेटा और डेमो सेटिंग्स इसी ब्राउज़र में रहती हैं। प्रोटोटाइप के लिए सर्वर जरूरी नहीं है।',
  helpHero:'बिना उलझन के मदद।',helpDesc:'प्रोटोटाइप इस्तेमाल करने के छोटे और आसान जवाब।',faq1Q:'जोखिम कैसे देखें?',faq1A:'एरिया सेफ्टी खोलें, 30 रिसर्च लोकेशन में से जगह चुनें और सुरक्षा देखें दबाएँ।',faq2Q:'क्या इंटरनेट जरूरी है?',faq2A:'मुख्य प्रोटोटाइप ऑफलाइन चलता है। इंटरनेट केवल बाहरी आधिकारिक स्रोत पेज खोलने के लिए चाहिए।',faq3Q:'रिस्क स्कोर लाइव क्यों नहीं है?',faq3A:'यह रिसर्च पर आधारित प्रोजेक्ट स्कोर है। प्रोडक्शन वर्जन में लाइव मौसम, सेंसर और प्राधिकरण अलर्ट जुड़ेंगे।',faq4Q:'मेरा डेटा कहाँ सेव होता है?',faq4A:'डेमो सेटिंग्स और सेव की गई जगहें आपके ब्राउज़र में लोकल रूप से सेव होती हैं।',
  loginVisualTitle:'स्थानीय सुरक्षा, अब आसान।',loginVisualDesc:'जोखिम विवरण, मैप मार्गदर्शन, अलर्ट और बदलाव पहचान एक शांत और सरल अनुभव में।',loginFoot:'ऑफलाइन प्रोटोटाइप · 30 रिसर्च लोकेशन',loginTitle:'वापस स्वागत है',loginSub:'अपने सुरक्षा डैशबोर्ड पर जाने के लिए साइन इन करें।',email:'ईमेल',password:'पासवर्ड',login:'साइन इन',demo:'डेमो अकाउंट इस्तेमाल करें',loginError:'सही ईमेल और कम से कम 4 अक्षर का पासवर्ड दर्ज करें।',
  verifyVisualTitle:'एक छोटा सत्यापन, फिर आप अंदर हैं।',verifyVisualDesc:'साफ डेमो सत्यापन जो पूरी तरह ऑफलाइन काम करता है।',verifyFoot:'किसी नेटवर्क रिक्वेस्ट की जरूरत नहीं',verifyTitle:'अपना अकाउंट सत्यापित करें',verifySub:'इस ईमेल पर भेजा गया 6 अंकों का डेमो कोड दर्ज करें',verify:'सत्यापित करके आगे बढ़ें',resend:'कोड फिर भेजें',verifyNote:'इस ऑफलाइन प्रोटोटाइप के लिए कोड 123456 इस्तेमाल करें।',verifyError:'6 अंकों का डेमो कोड 123456 दर्ज करें।',resendDone:'डेमो कोड 123456 है।',
  sourceNotePrefix:'आधिकारिक SSDMA रिसर्च संदर्भ',high:'उच्च',medium:'मध्यम',low:'कम',risk:'जोखिम',district:'जिला',
 },
 hinglish:{
  main:'MAIN',tools:'TOOLS',account:'ACCOUNT',home:'Home',map:'Map',alerts:'Alerts',assistant:'AI Assistant',safety:'Area Safety',change:'Change Detection',saved:'Saved Places',settings:'Settings',help:'Help & Support',
  yourArea:'Your area',welcome:'Welcome',logout:'Log out',profileMenuSettings:'Settings',profileMenuSaved:'Saved places',
  homeEyebrow:'AAJ KA AREA UPDATE',homeTitle:'Good morning,',homeDesc:'Selected area ki safety ka clear aur simple snapshot.',viewSafety:'Area safety dekho',openMap:'Map kholo',currentRisk:'Current risk',primaryRisk:'Main risk',whyRisk:'Risk kyu hai?',weather:'Weather',weatherText:'Abhi weather comfortable hai',rain:'Rain',wind:'Wind',humidity:'Humidity',researchPreview:'Research based safety preview.',researchMarkers:'30 researched locations clear risk markers ke saath.',changeCardText:'Old aur new image ko simple flow me compare karo.',savedCardText:'Important places ko one tap me kholo.',
  safetyHero:'Move karne se pehle risk jaan lo.',safetyDesc:'Research location choose karo aur risk, reason, warning signs, safer timing aur route guidance clearly dekho.',researchLocations:'30 verified locations · offline available',checkLocation:'Location check karo',searchResearch:'30 verified Sikkim research cases me search karo',checkSafety:'Safety check karo',locationNotFound:'Matching researched location nahi mili. Suggestions me se koi place choose karo.',riskScore:'research risk score',warningSigns:'Warning signs',safetySteps:'Safety steps',riskReduction:'Risk kab kam ho sakta hai',safeRoute:'Safer place / route',officialSource:'Verified research source',openSource:'Official source kholo',datasetNote:'Ye research based prototype score hai, live government warning nahi. Current official alerts ko follow karo.',mapOpen:'Map kholo',
  mapHero:'Apne aas-paas ka risk dekho.',mapDesc:'Research locations explore karo, risk level filter karo aur one tap me safety details kholo.',allLocations:'All locations',highRisk:'High risk',mediumRisk:'Medium risk',lowRisk:'Low risk',selectedLocation:'Selected location',viewDetails:'Details dekho',selectMarker:'Marker select karo',verifiedLocations:'30 verified research locations',
  alertsHero:'Sirf important alerts.',alertsDesc:'Important warnings aur safety reminders, simple aur readable form me.',markRead:'Sab read mark karo',unreadAlerts:'unread alerts',allCaughtUp:'Sab alerts read ho gaye',markThisRead:'Read mark karo',read:'Read',
  alert1Title:'Heavy rainfall watch',alert1Body:'Rain continue hui to landslide-prone roads unstable ho sakti hain.',alert1Time:'12 min pehle',alert2Title:'Road caution',alert2Body:'Steep slopes ke paas sirf officially opened routes use karo.',alert2Time:'38 min pehle',alert3Title:'Daily safety tip',alert3Body:'Emergency numbers aur ek offline map screenshot ready rakho.',alert3Time:'2 hr pehle',alert4Title:'Teesta corridor reminder',alert4Body:'Official flood warning ke time low-lying riverbank areas avoid karo.',alert4Time:'5 hr pehle',
  aiHero:'Safety ke baare me simple language me pucho.',aiDesc:'Common risk, travel aur emergency questions ke liye offline demo assistant.',typeQuestion:'Apna question type karo…',send:'Send',quick1:'Kya ye landslide area safe hai?',quick2:'Flood me kya karu?',quick3:'Safer route kaise dekhu?',aiGreeting:'Hi! Local risk, safer routes, flood ya landslide precautions ke baare me pucho.',aiFlood:'Riverbank aur low-lying area se door jao, flood water cross mat karo aur official alerts follow karo. Location-specific guidance ke liye Area Safety kholo.',aiLandslide:'Heavy rain me steep ya unstable slopes aur fresh debris/cracks wali roads avoid karo. Sirf officially reopened routes use karo.',aiRoute:'Selected location ke liye Area Safety kholo, phir safer route guidance aur Map button use karo. Route ko current local advisory se confirm karo.',aiEmergency:'Immediate danger ho to safer open ya higher area me jao aur local emergency instructions follow karo. Blocked road ya active hazard zone me mat jao.',aiFallback:'Main flood, landslide, road safety, safer routes aur BhuDrishti features me help kar sakta hu. Inme se kuch pucho.',
  changeHero:'Clearly dekho kya change hua.',changeDesc:'Old aur new image compare karke simple change summary dekho, technical dashboard nahi.',olderImage:'Older image',newerImage:'Newer image',chooseImage:'Image choose karo',compare:'Images compare karo',trySample:'Sample try karo',changeSummary:'Change summary',possibleImpact:'Possible impact',suggestedAction:'Suggested action',changePercent:'Change detected',noImages:'Compare karne ke liye dono images add karo.',samplePrompt:'Images upload karo ya pehle sample try karo.',sampleSummary:'Sample pair me visible surface aur land-cover change detect hua.',sampleImpact:'Road, slope ya water channel ke paas change ho to extra safety review useful hoga.',sampleAction:'Changed zone review karo aur current weather aur local risk info ke saath compare karo.',
  savedHero:'Important places one tap away rakho.',savedDesc:'Important locations save karo aur unki safety details quickly kholo.',addPlace:'Place save karo',searchPlaces:'Location search karo',noSaved:'Abhi koi place saved nahi hai. Upar researched location search karke save karo.',remove:'Remove',
  settingsHero:'BhuDrishti ko apne hisaab se set karo.',settingsDesc:'Language, theme aur simple notification preferences choose karo.',appearance:'Appearance',appearanceDesc:'Comfortable theme choose karo.',language:'Language',languageDesc:'Full interface me English, Hindi ya Hinglish choose karo.',light:'Light',dark:'Dark',profile:'Profile',displayName:'Display name',save:'Save changes',notifications:'Notifications',riskAlerts:'Risk alerts',riskAlertsDesc:'Important location-risk notifications dikhao.',weatherAlerts:'Weather alerts',weatherAlertsDesc:'Weather related safety notifications dikhao.',data:'DATA',offlinePrototype:'Offline prototype',offlineDesc:'Research data aur demo preferences isi browser me store hote hain. Prototype ke liye server required nahi hai.',
  helpHero:'Help, bina hassle ke.',helpDesc:'Prototype use karne ke quick aur simple answers.',faq1Q:'Risk kaise check karu?',faq1A:'Area Safety kholo, 30 researched locations me se place choose karo aur Check safety press karo.',faq2Q:'Internet chahiye?',faq2A:'Main prototype offline work karta hai. Internet sirf external official source pages open karne ke liye chahiye.',faq3Q:'Risk score live kyu nahi hai?',faq3A:'Ye research based project score hai. Production version me live weather, sensors aur authority alerts combine honge.',faq4Q:'Mera data kaha store hota hai?',faq4A:'Demo preferences aur saved places browser me locally store hote hain.',
  loginVisualTitle:'Local safety, simple bana di.',loginVisualDesc:'Risk details, map guidance, alerts aur change detection ek calm user experience me.',loginFoot:'Offline-ready prototype · 30 researched locations',loginTitle:'Welcome back',loginSub:'Safety dashboard continue karne ke liye sign in karo.',email:'Email',password:'Password',login:'Sign in',demo:'Demo account use karo',loginError:'Valid email aur minimum 4 character password enter karo.',
  verifyVisualTitle:'Ek quick check. Phir dashboard open.',verifyVisualDesc:'Clean demo verification jo fully offline work karta hai.',verifyFoot:'Network request required nahi hai',verifyTitle:'Account verify karo',verifySub:'Is email par bheja 6-digit demo code enter karo',verify:'Verify & continue',resend:'Code resend karo',verifyNote:'Offline prototype ke liye code 123456 use karo.',verifyError:'6-digit demo code 123456 enter karo.',resendDone:'Demo code 123456 hai.',
  sourceNotePrefix:'Official SSDMA research reference',high:'High',medium:'Medium',low:'Low',risk:'risk',district:'District',
 }
};
const ICONS={home:'<svg viewBox="0 0 24 24"><path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v10h13V10"/><path d="M9.5 20v-6h5v6"/></svg>',map:'<svg viewBox="0 0 24 24"><path d="m3 6 5-2 8 3 5-2v13l-5 2-8-3-5 2Z"/><path d="M8 4v13M16 7v13"/></svg>',alerts:'<svg viewBox="0 0 24 24"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/><path d="M10 21h4"/></svg>',assistant:'<svg viewBox="0 0 24 24"><path d="M4 5h16v12H8l-4 3Z"/><path d="M8 9h8M8 13h5"/></svg>',safety:'<svg viewBox="0 0 24 24"><path d="M12 3 5 6v5c0 4.6 2.8 8 7 10 4.2-2 7-5.4 7-10V6Z"/><path d="m9 12 2 2 4-4"/></svg>',change:'<svg viewBox="0 0 24 24"><path d="M7 7h11l-3-3M17 17H6l3 3"/><path d="m18 7-3 3M6 17l3-3"/></svg>',saved:'<svg viewBox="0 0 24 24"><path d="M6 4h12v17l-6-4-6 4Z"/></svg>',settings:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5V21h-4v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9A1.7 1.7 0 0 0 3.1 14H3v-4h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.9L4.2 7 7 4.2l.1.1a1.7 1.7 0 0 0 1.9.3 1.7 1.7 0 0 0 1-1.5V3h4v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.5 1h.1v4h-.1a1.7 1.7 0 0 0-1.5 1Z"/></svg>',help:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.8 9a2.3 2.3 0 1 1 3.5 2c-.8.5-1.3 1-1.3 2M12 17h.01"/></svg>',theme:'<svg viewBox="0 0 24 24"><path d="M20.5 15.6A8.5 8.5 0 0 1 8.4 3.5 8.5 8.5 0 1 0 20.5 15.6Z"/></svg>',menu:'<svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',pin:'<svg viewBox="0 0 24 24"><path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></svg>',search:'<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6"/><path d="m16 16 4 4"/></svg>',chevron:'<svg viewBox="0 0 24 24"><path d="m8 10 4 4 4-4"/></svg>',logout:'<svg viewBox="0 0 24 24"><path d="M10 4H5v16h5M14 8l4 4-4 4M18 12H9"/></svg>'};
function lang(){const l=localStorage.getItem(LANG_KEY)||'en';return T[l]?l:'en'}
function t(k){return (T[lang()]&&T[lang()][k])||T.en[k]||k}
function applyTranslations(root=document){document.documentElement.lang=lang()==='hi'?'hi':'en';root.querySelectorAll('[data-i18n]').forEach(el=>{const key=el.dataset.i18n;if(el.dataset.i18nAttr){el.setAttribute(el.dataset.i18nAttr,t(key))}else el.textContent=t(key)});root.querySelectorAll('[data-lang-select]').forEach(el=>el.value=lang());}
function setLanguage(l){if(!T[l])l='en';localStorage.setItem(LANG_KEY,l);applyTranslations();document.dispatchEvent(new CustomEvent('app:language',{detail:{language:l}}))}
function theme(){return localStorage.getItem(THEME_KEY)==='dark'?'dark':'light'}
function applyTheme(){document.documentElement.setAttribute('data-theme',theme())}
function setTheme(v){localStorage.setItem(THEME_KEY,v==='dark'?'dark':'light');applyTheme();document.dispatchEvent(new CustomEvent('app:theme'))}
function currentArea(){return localStorage.getItem(AREA_KEY)||'Sikkim, India'}
function setArea(v){if(v)localStorage.setItem(AREA_KEY,v);document.querySelectorAll('[data-current-area]').forEach(el=>el.textContent=currentArea())}
function user(){try{return JSON.parse(localStorage.getItem('bhudrishtiUser')||'{}')}catch(e){return{}}}
function userName(){return user().name||'Rohit'}
function localizeLevel(level){const key=String(level||'').toLowerCase();return t(key)||level}
function localizeRiskType(type){const l=lang();if(l==='en')return type;const hi={'Flood / GLOF':'बाढ़ / GLOF','Flood / Road Risk':'बाढ़ / सड़क जोखिम','Landslide':'भूस्खलन','Landslide / Road Risk':'भूस्खलन / सड़क जोखिम','Landslide / Rock-fall Risk':'भूस्खलन / चट्टान गिरने का जोखिम','Landslide / Subsidence Risk':'भूस्खलन / जमीन धँसने का जोखिम','Landslide / Road & Settlement Risk':'भूस्खलन / सड़क और बस्ती जोखिम','Landslide / Settlement Risk':'भूस्खलन / बस्ती जोखिम'};const hg={'Flood / GLOF':'Flood / GLOF','Flood / Road Risk':'Flood / road risk','Landslide':'Landslide','Landslide / Road Risk':'Landslide / road risk','Landslide / Rock-fall Risk':'Landslide / rock-fall risk','Landslide / Subsidence Risk':'Landslide / ground-subsidence risk','Landslide / Road & Settlement Risk':'Landslide / road & settlement risk','Landslide / Settlement Risk':'Landslide / settlement risk'};return (l==='hi'?hi:hg)[type]||type}
function localizedRisk(item){if(lang()==='en')return {reason:item['Risk Reason'],warnings:split(item['Warning Signs']),safety:split(item['Safety Precautions']),recovery:item['Approx. When Risk May Reduce'],route:item['Alternative Safe Location/Route'],source:item['Official Document / Section to Check'],note:item['Verification Note']};const type=item['Risk Type']||'';const flood=type.includes('Flood')||type.includes('GLOF');const subs=type.includes('Subsidence');const rock=type.includes('Rock-fall');const settlement=type.includes('Settlement');if(lang()==='hi')return {reason:flood?`${item['Location Name']} SSDMA के आधिकारिक रिकॉर्ड में बाढ़/GLOF जोखिम से जुड़ा क्षेत्र है। नदी या जलस्तर में तेज बढ़ोतरी, भारी बारिश या अपस्ट्रीम चेतावनी के समय जोखिम बढ़ सकता है।`:subs?`${item['Location Name']} में जमीन धँसने और ढलान अस्थिरता का रिकॉर्ड है। भूजल, दरारें और जमीन की हलचल जोखिम बढ़ा सकती हैं।`:rock?`${item['Location Name']} में चट्टान गिरने और ढलान अस्थिरता का दर्ज जोखिम है। बारिश, कमजोर चट्टान और खड़ी ढलान जोखिम बढ़ा सकते हैं।`:`${item['Location Name']} SSDMA रिसर्च में भूस्खलन/ढलान अस्थिरता से जुड़ा स्थान है। भारी बारिश, कमजोर मिट्टी या चट्टान, भूजल और खड़ी ढलान जोखिम बढ़ा सकते हैं।`,warnings:flood?['नदी या जलस्तर तेजी से बढ़ना','भारी या लगातार बारिश','आधिकारिक बाढ़/GLOF चेतावनी','पानी में अधिक मलबा या असामान्य बहाव']:subs?['जमीन या सड़क में नई दरारें','जमीन धँसना या असमान होना','असामान्य रिसाव या बहुत गीली मिट्टी','इमारत या सड़क में अचानक झुकाव']:rock?['ढलान से पत्थर या बोल्डर गिरना','चट्टानों में नई दरारें','सड़क पर ताजा मलबा','बारिश के बाद गिरावट बढ़ना']:['नई दरारें या ढलान की हलचल','पत्थर/मिट्टी या ताजा मलबा गिरना','पानी का रिसाव या गंदा बहाव','भारी बारिश के बाद सड़क या ढलान बदलना'],safety:flood?['नदी किनारे और निचले क्षेत्र से दूर जाएँ','बाढ़ के पानी को पार न करें','आधिकारिक अलर्ट और निकासी निर्देश मानें','जरूरत पर ऊँचे या सुरक्षित स्थान पर जाएँ']:['अस्थिर ढलान और ताजा मलबे से दूर रहें','बंद सड़क या सक्रिय स्लाइड क्षेत्र में न जाएँ','केवल आधिकारिक रूप से खुले मार्ग का उपयोग करें','निकासी निर्देश मिलने पर सुरक्षित खुले क्षेत्र में जाएँ'],recovery:flood?'कोई तय सुरक्षित समय नहीं है। जलस्तर और बारिश कम होने तथा अधिकारियों के सुरक्षित घोषित करने के बाद ही तत्काल जोखिम कम माना जाए।':'कोई तय सुरक्षित समय नहीं है। बारिश/भूजल और ढलान की हलचल कम होने तथा सड़क या क्षेत्र की आधिकारिक जाँच के बाद ही जोखिम कम माना जाए।',route:flood?'ऊँचे सुरक्षित स्थान या आधिकारिक रूप से खुले मार्ग का उपयोग करें। नदी किनारे की सड़क और क्षतिग्रस्त पुल से बचें।':'केवल आधिकारिक रूप से घोषित डायवर्जन या खुले मार्ग का उपयोग करें। प्रभावित ढलान/सड़क से बचें।',source:`आधिकारिक SSDMA दस्तावेज: ${item['Official Document / Section to Check']}`,note:`${t('sourceNotePrefix')}. यह ${localizeLevel(item['Risk Level'])} जोखिम वर्गीकरण प्रोजेक्ट रिसर्च के लिए है, लाइव सरकारी अलर्ट नहीं।`};return {reason:flood?`${item['Location Name']} official SSDMA records me flood/GLOF risk se linked area hai. Fast river rise, heavy rain ya upstream warning ke time risk badh sakta hai.`:subs?`${item['Location Name']} me ground subsidence aur slope instability ka recorded risk hai. Groundwater, cracks aur ground movement risk badha sakte hain.`:rock?`${item['Location Name']} me rock-fall aur slope instability ka recorded risk hai. Rain, weak rock aur steep slope risk badha sakte hain.`:`${item['Location Name']} SSDMA research me landslide/slope instability se linked location hai. Heavy rain, weak soil/rock, groundwater aur steep slope risk badha sakte hain.`,warnings:flood?['River ya water level fast badhna','Heavy ya prolonged rain','Official flood/GLOF warning','Debris-heavy ya unusual water flow']:subs?['Ground ya road me new cracks','Ground sinking ya uneven hona','Unusual seepage / bahut wet soil','Road/building me sudden tilt']:rock?['Slope se rock/boulder fall','Rock face me new cracks','Road par fresh debris','Rain ke baad rock fall badhna']:['New cracks ya slope movement','Fresh rock/soil/debris fall','Seepage ya muddy runoff','Heavy rain ke baad road/slope change'],safety:flood?['Riverbank aur low-lying area se door raho','Flood water cross mat karo','Official alerts aur evacuation instructions follow karo','Need ho to higher/safe ground par jao']:['Unstable slope aur fresh debris se door raho','Closed road ya active slide zone me mat jao','Sirf officially opened route use karo','Evacuation instruction mile to safe open area me jao'],recovery:flood?'Fixed safe time nahi hai. Water level/rain kam hone aur authority ke all-clear ke baad hi immediate risk lower maana jayega.':'Fixed safe time nahi hai. Rain/groundwater aur slope movement stabilize hone aur official inspection ke baad hi risk lower maana jayega.',route:flood?'Higher safe area ya officially opened route use karo. Riverbank roads aur damaged bridges avoid karo.':'Sirf officially announced diversion/open route use karo. Affected slope/road avoid karo.',source:`Official SSDMA document: ${item['Official Document / Section to Check']}`,note:`${t('sourceNotePrefix')}. Ye ${localizeLevel(item['Risk Level'])} risk classification project research ke liye hai, live government alert nahi.`}}
function split(s){return String(s||'').split(';').map(x=>x.trim()).filter(Boolean)}
function getReadIds(){try{return JSON.parse(localStorage.getItem(READ_KEY)||'[]')}catch(e){return[]}}
function setReadIds(ids){localStorage.setItem(READ_KEY,JSON.stringify(ids));updateAlertBadges();document.dispatchEvent(new CustomEvent('app:alerts'))}
function alertIds(){return ['a1','a2','a3','a4']}
function unreadCount(){const read=new Set(getReadIds());return alertIds().filter(id=>!read.has(id)).length}
function updateAlertBadges(){const n=unreadCount();document.querySelectorAll('[data-alert-badge]').forEach(el=>{el.textContent=n;el.hidden=n===0})}
function markAllRead(){setReadIds(alertIds())}
function injectIcons(){document.querySelectorAll('[data-icon]').forEach(el=>{const s=ICONS[el.dataset.icon];if(s)el.innerHTML=s})}
function setupSidebarScrollPersistence(){const scroller=document.querySelector('.sidebar-main');if(!scroller)return;const key='bhudrishtiSidebarScroll';const save=()=>{try{sessionStorage.setItem(key,String(scroller.scrollTop))}catch(e){}};const restore=()=>{try{const y=Number(sessionStorage.getItem(key)||0);if(Number.isFinite(y))scroller.scrollTop=y}catch(e){}};requestAnimationFrame(()=>requestAnimationFrame(restore));let frame=0;scroller.addEventListener('scroll',()=>{cancelAnimationFrame(frame);frame=requestAnimationFrame(save)},{passive:true});document.querySelectorAll('.sidebar a[href]').forEach(a=>a.addEventListener('click',save));window.addEventListener('pagehide',save);window.addEventListener('beforeunload',save)}
function languageLabel(code) {
  if (code === 'hi') return 'हिंदी';
  if (code === 'hinglish') return 'Hinglish';
  return 'English';
}

let activeLanguagePicker = null;

function closeLanguagePicker(picker = activeLanguagePicker) {
  if (!picker) return;

  picker.classList.remove('open');
  const trigger = picker.querySelector('.language-picker-trigger');
  const menu = picker._menu;

  if (trigger) trigger.setAttribute('aria-expanded', 'false');
  if (menu) menu.classList.remove('open');

  if (activeLanguagePicker === picker) activeLanguagePicker = null;
}

function closeLanguagePickers(except = null) {
  document.querySelectorAll('.language-picker.open').forEach((picker) => {
    if (picker !== except) closeLanguagePicker(picker);
  });
}

function positionLanguageMenu(picker) {
  const trigger = picker.querySelector('.language-picker-trigger');
  const menu = picker._menu;
  if (!trigger || !menu) return;

  const rect = trigger.getBoundingClientRect();
  const viewportPadding = 10;
  const menuWidth = Math.max(164, Math.round(rect.width));

  menu.style.width = `${menuWidth}px`;
  menu.style.visibility = 'hidden';
  menu.classList.add('open');

  const measuredHeight = menu.offsetHeight || 150;
  let left = rect.right - menuWidth;
  left = Math.max(viewportPadding, Math.min(left, window.innerWidth - menuWidth - viewportPadding));

  let top = rect.bottom + 8;
  if (top + measuredHeight > window.innerHeight - viewportPadding) {
    top = Math.max(viewportPadding, rect.top - measuredHeight - 8);
  }

  menu.style.left = `${Math.round(left)}px`;
  menu.style.top = `${Math.round(top)}px`;
  menu.style.visibility = 'visible';
}

function enhanceLanguagePicker(select) {
  if (!select || select.dataset.enhanced === 'true') return;

  select.dataset.enhanced = 'true';
  select.classList.add('native-language-select');
  select.tabIndex = -1;
  select.setAttribute('aria-hidden', 'true');

  const picker = document.createElement('div');
  picker.className = 'language-picker';

  const trigger = document.createElement('button');
  trigger.type = 'button';
  trigger.className = 'language-picker-trigger';
  trigger.setAttribute('aria-haspopup', 'listbox');
  trigger.setAttribute('aria-expanded', 'false');
  trigger.innerHTML = [
    '<span class="language-picker-label"></span>',
    '<span class="language-picker-chevron" aria-hidden="true">⌄</span>'
  ].join('');

  const menu = document.createElement('div');
  menu.className = 'language-picker-menu language-picker-portal';
  menu.setAttribute('role', 'listbox');
  menu.setAttribute('aria-label', 'Language');

  Array.from(select.options).forEach((option) => {
    const item = document.createElement('button');
    item.type = 'button';
    item.className = 'language-picker-option';
    item.dataset.value = option.value;
    item.setAttribute('role', 'option');
    item.textContent = option.textContent.trim();

    item.addEventListener('click', (event) => {
      event.stopPropagation();
      select.value = option.value;
      setLanguage(option.value);
      closeLanguagePicker(picker);
    });

    menu.appendChild(item);
  });

  picker.appendChild(trigger);
  select.insertAdjacentElement('afterend', picker);
  document.body.appendChild(menu);
  picker._menu = menu;

  function sync() {
    const active = lang();
    select.value = active;

    const label = picker.querySelector('.language-picker-label');
    if (label) label.textContent = languageLabel(active);

    menu.querySelectorAll('.language-picker-option').forEach((item) => {
      const selected = item.dataset.value === active;
      item.classList.toggle('active', selected);
      item.setAttribute('aria-selected', selected ? 'true' : 'false');
    });
  }

  trigger.addEventListener('click', (event) => {
    event.stopPropagation();

    const shouldOpen = !picker.classList.contains('open');
    closeLanguagePickers(picker);

    if (!shouldOpen) {
      closeLanguagePicker(picker);
      return;
    }

    picker.classList.add('open');
    trigger.setAttribute('aria-expanded', 'true');
    activeLanguagePicker = picker;
    positionLanguageMenu(picker);
  });

  document.addEventListener('app:language', sync);
  sync();
}

function setupLanguagePickers() {
  document.querySelectorAll('[data-lang-select]').forEach(enhanceLanguagePicker);

  document.addEventListener('click', () => closeLanguagePickers());
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeLanguagePickers();
  });

  window.addEventListener('resize', () => closeLanguagePickers(), { passive: true });
  window.addEventListener('scroll', () => closeLanguagePickers(), { passive: true, capture: true });
}

function setupSidebarControls() {
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.mobile-overlay');
  const buttons = Array.from(document.querySelectorAll('[data-menu-toggle]'));
  const desktopKey = 'bhudrishtiSidebarCollapsed';
  const mobileQuery = window.matchMedia('(max-width: 840px)');

  if (!sidebar || buttons.length === 0) return;

  function isMobileLayout() {
    return mobileQuery.matches;
  }

  function setButtonState(expanded) {
    buttons.forEach((button) => button.setAttribute('aria-expanded', expanded ? 'true' : 'false'));
  }

  function closeMobileDrawer() {
    sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('show');
    document.body.classList.remove('drawer-open');
    setButtonState(false);
  }

  function syncDesktopState() {
    if (isMobileLayout()) {
      document.body.classList.remove('sidebar-collapsed');
      return;
    }

    const collapsed = localStorage.getItem(desktopKey) === 'true';
    document.body.classList.toggle('sidebar-collapsed', collapsed);
    sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('show');
    document.body.classList.remove('drawer-open');
    setButtonState(!collapsed);
  }

  function toggleSidebar() {
    closeLanguagePickers();

    if (isMobileLayout()) {
      const opening = !sidebar.classList.contains('open');
      sidebar.classList.toggle('open', opening);
      if (overlay) overlay.classList.toggle('show', opening);
      document.body.classList.toggle('drawer-open', opening);
      setButtonState(opening);
      return;
    }

    const collapsed = !document.body.classList.contains('sidebar-collapsed');
    document.body.classList.toggle('sidebar-collapsed', collapsed);
    localStorage.setItem(desktopKey, String(collapsed));
    setButtonState(!collapsed);
  }

  buttons.forEach((button) => {
    button.setAttribute('aria-controls', 'app-sidebar');
    button.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      toggleSidebar();
    });
  });

  sidebar.id = 'app-sidebar';

  if (overlay) overlay.addEventListener('click', closeMobileDrawer);

  sidebar.querySelectorAll('a[href]').forEach((link) => {
    link.addEventListener('click', () => {
      if (isMobileLayout()) closeMobileDrawer();
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && isMobileLayout()) closeMobileDrawer();
  });

  mobileQuery.addEventListener?.('change', () => {
    closeMobileDrawer();
    syncDesktopState();
  });

  syncDesktopState();
}

function setupShell() {
  applyTheme();
  injectIcons();
  applyTranslations();
  setArea(currentArea());

  document.querySelectorAll('[data-user-name]').forEach((element) => {
    element.textContent = userName();
  });

  document.querySelectorAll('[data-user-initial]').forEach((element) => {
    element.textContent = userName().trim().charAt(0).toUpperCase() || 'U';
  });

  setupLanguagePickers();
  setupSidebarControls();

  document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      setTheme(theme() === 'dark' ? 'light' : 'dark');
      closeLanguagePickers();
    });
  });

  const profileButton = document.querySelector('[data-profile-toggle]');
  const profileMenu = document.querySelector('.profile-menu');

  if (profileButton) {
    profileButton.addEventListener('click', (event) => {
      event.stopPropagation();
      if (profileMenu) profileMenu.classList.toggle('open');
      closeLanguagePickers();
    });
  }

  document.addEventListener('click', () => {
    if (profileMenu) profileMenu.classList.remove('open');
  });

  document.querySelectorAll('[data-logout]').forEach((button) => {
    button.addEventListener('click', () => {
      localStorage.removeItem('bhudrishtiVerified');
      window.location.href = 'index.html';
    });
  });

  updateAlertBadges();
  setupSidebarScrollPersistence();
}
document.addEventListener('DOMContentLoaded',setupShell);
window.BhuApp={t,lang,setLanguage,theme,setTheme,currentArea,setArea,user,userName,applyTranslations,localizeLevel,localizeRiskType,localizedRisk,split,getReadIds,setReadIds,alertIds,unreadCount,updateAlertBadges,markAllRead};
})();
