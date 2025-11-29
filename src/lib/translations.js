import { writable, derived } from 'svelte/store';

// Language store
export const currentLanguage = writable('en');

// Translation dictionary
export const translations = {
  en: {
    // Navigation
    home: 'Home',
    reportLost: 'Report Lost',
    reportFound: 'Report Found',
    about: 'About',
    contact: 'Contact',
    getStarted: 'Get Started',
    
    // Hero Section
    heroTitle: 'ISHAKIRO',
    heroSubtitle: 'Reuniting Lost Items with AI Technology',
    heroDescription: 'Report lost or found items in 30 seconds. No registration required.',
    iLostSomething: 'I Lost Something',
    iFoundSomething: 'I Found Something',
    
    // Features
    quickReporting: 'Quick Reporting',
    aiMatching: 'AI Matching',
    liveChat: 'Live Chat',
    mobileMoney: 'Mobile Money',
    thirtySeconds: '30 Seconds',
    smartAlgorithm: 'Smart Algorithm',
    realTimeMessaging: 'Real-time Messaging',
    mtnAirtel: 'MTN & Airtel',
    
    // Recent Items
    recentItems: 'Recent Items',
    browseDescription: 'Browse lost and found items reported by the community',
    allItems: 'All Items',
    lost: 'Lost',
    found: 'Found',
    loadingItems: 'Loading items...',
    noItemsYet: 'No {filter} items yet',
    beFirstToReport: 'Be the first to report an item!',
    reportLostItem: 'Report Lost Item',
    reportFoundItem: 'Report Found Item',
    reportedBy: 'Reported by',
    
    // Forms
    yourInformation: 'Your Information',
    fullName: 'Full Name',
    phoneNumber: 'Phone Number',
    itemDetails: 'Item Details',
    itemTitle: 'Item Title',
    category: 'Category',
    detailedDescription: 'Detailed Description',
    locationInformation: 'Location Information',
    whereDidYouLoseIt: 'Where did you lose it?',
    whereDidYouFindIt: 'Where did you find it?',
    useGPS: 'Use GPS',
    required: '*',
    
    // Categories
    phone: 'Phone',
    wallet: 'Wallet',
    keys: 'Keys',
    bag: 'Bag',
    documents: 'Documents',
    electronics: 'Electronics',
    jewelry: 'Jewelry',
    other: 'Other',
    
    // Buttons
    submit: 'Submit',
    sendMessage: 'Send Message',
    cancel: 'Cancel',
    save: 'Save',
    delete: 'Delete',
    edit: 'Edit',
    
    // About Page
    aboutTitle: 'About Ishakiro',
    aboutDescription: "We're on a mission to reunite lost items with their owners using AI technology and community spirit in Rwanda.",
    ourMission: 'Our Mission',
    missionDescription: 'To create a seamless, AI-powered platform that connects people who have lost items with those who have found them.',
    freeToReport: '100% Free to report items',
    aiPoweredMatching: 'AI-powered matching technology',
    madeForRwanda: 'Made with ❤️ for Rwanda',
    howItWorks: 'How It Works',
    report: 'Report',
    aiMatch: 'AI Match',
    connect: 'Connect',
    reportDescription: 'Report your lost or found item in 30 seconds.',
    aiMatchDescription: 'Our AI finds the best matches automatically.',
    connectDescription: 'Chat securely to arrange item return.',
    
    // Contact Page
    contactTitle: 'Contact Us',
    contactDescription: "Have questions? Need help? We're here to assist you 24/7.",
    sendUsMessage: 'Send us a Message',
    emailAddress: 'Email Address',
    subject: 'Subject',
    message: 'Message',
    getInTouch: 'Get in Touch',
    businessHours: 'Business Hours',
    quickHelp: 'Quick Help',
    
    // Footer
    quickLinks: 'Quick Links',
    support: 'Support',
    helpCenter: 'Help Center',
    privacyPolicy: 'Privacy Policy',
    termsOfService: 'Terms of Service',
    poweredByAI: 'Powered by AI',
    systemOnline: 'System Online',
    madeWithLove: 'Made with ❤️ for Rwanda',
    
    // Messages
    fillAllFields: 'Please fill in all required fields',
    itemReportedSuccess: 'Item reported successfully!',
    trackingCode: 'Tracking Code',
    saveTrackingCode: 'Save this code to track your item.',
    messageSentSuccess: 'Message sent successfully! We will get back to you within 24 hours.',
    
    // Placeholders
    enterFullName: 'Enter your full name',
    enterPhoneNumber: '+250 788 123 456',
    enterItemTitle: 'e.g., Black iPhone 13 Pro',
    enterDescription: 'Describe your item in detail: color, brand, model, distinctive features, where you lost it, etc.',
    enterLocation: 'e.g., Kigali City Market, Nyabugogo Bus Station',
    enterEmail: 'your.email@example.com',
    enterSubject: 'What is this about?',
    enterMessage: 'Tell us how we can help you...',
    
    // Tips
    tipsForBetter: 'Tips for Better Results',
    beSpecific: 'Be specific: Include brand, model, color, and unique features',
    mentionLocation: 'Mention location details: Exact place, nearby landmarks',
    checkRegularly: 'Check back regularly: New found items are added daily',
    keepPhoneOn: "Keep your phone on: We'll contact you when matches are found",
    
    // Image Upload
    uploadImage: 'Upload Image (Optional)',
    chooseImage: 'Choose Image',
    imageHelp: 'Upload a photo to help with AI matching',
    maxFileSize: 'Max file size: 5MB',
    supportedFormats: 'Supported: JPG, PNG, WEBP'
  },
  
  rw: {
    // Navigation
    home: 'Ahabanza',
    reportLost: 'Tanga Ikintu Cyabuze',
    reportFound: 'Tanga Ikintu Wasanze',
    about: 'Ibibazo',
    contact: 'Twandikire',
    getStarted: 'Tangira',
    
    // Hero Section
    heroTitle: 'ISHAKIRO',
    heroSubtitle: 'Guhuriza Ibintu Byabuze n\'Ikoranabuhanga rya AI',
    heroDescription: 'Tanga ibintu byabuze cyangwa wasanze mu masegonda 30. Ntukeneye kwiyandikisha.',
    iLostSomething: 'Nabuze Ikintu',
    iFoundSomething: 'Nasanze Ikintu',
    
    // Features
    quickReporting: 'Gutanga Byihuse',
    aiMatching: 'Guhuriza kwa AI',
    liveChat: 'Ikiganiro Cyihuse',
    mobileMoney: 'Amafaranga ya Telefoni',
    thirtySeconds: 'Amasegonda 30',
    smartAlgorithm: 'Algorithm Yubwenge',
    realTimeMessaging: 'Ubutumwa bwihuse',
    mtnAirtel: 'MTN & Airtel',
    
    // Recent Items
    recentItems: 'Ibintu Bigezweho',
    browseDescription: 'Reba ibintu byabuze kandi byasanzwe byatanzwe n\'abaturage',
    allItems: 'Ibintu Byose',
    lost: 'Byabuze',
    found: 'Byasanzwe',
    loadingItems: 'Birashakishwa...',
    noItemsYet: 'Nta bintu {filter} bigezweho',
    beFirstToReport: 'Ba uwambere gutanga ikintu!',
    reportLostItem: 'Tanga Ikintu Cyabuze',
    reportFoundItem: 'Tanga Ikintu Wasanze',
    reportedBy: 'Byatanzwe na',
    
    // Forms
    yourInformation: 'Amakuru Yawe',
    fullName: 'Amazina Yose',
    phoneNumber: 'Nimero ya Telefoni',
    itemDetails: 'Ibisobanuro by\'Ikintu',
    itemTitle: 'Izina ry\'Ikintu',
    category: 'Icyiciro',
    detailedDescription: 'Ibisobanuro Birambuye',
    locationInformation: 'Amakuru y\'Ahantu',
    whereDidYouLoseIt: 'Wabuzeyehe?',
    whereDidYouFindIt: 'Wasanzeyehe?',
    useGPS: 'Koresha GPS',
    required: '*',
    
    // Categories
    phone: 'Telefoni',
    wallet: 'Amafaranga',
    keys: 'Urufunguzo',
    bag: 'Umufuka',
    documents: 'Inyandiko',
    electronics: 'Ibikoresho bya Elegitoronike',
    jewelry: 'Imitako',
    other: 'Ikindi',
    
    // Buttons
    submit: 'Ohereza',
    sendMessage: 'Ohereza Ubutumwa',
    cancel: 'Hagarika',
    save: 'Bika',
    delete: 'Siba',
    edit: 'Hindura',
    
    // About Page
    aboutTitle: 'Ibibazo kuri Ishakiro',
    aboutDescription: 'Tugamije guhuriza ibintu byabuze n\'abanyir\'ibyo dukoresheje ikoranabuhanga rya AI n\'ubwiyunge bw\'abaturage mu Rwanda.',
    ourMission: 'Intego Yacu',
    missionDescription: 'Kurema urubuga rworoshye, rukoresha AI, ruhuriza abantu babuze ibintu n\'abababisanze.',
    freeToReport: '100% Ubuntu gutanga ibintu',
    aiPoweredMatching: 'Ikoranabuhanga ryo guhuriza rya AI',
    madeForRwanda: 'Ryakozwe n\'urukundo rwa Rwanda',
    howItWorks: 'Ukuntu Bikora',
    report: 'Tanga',
    aiMatch: 'AI Ihurize',
    connect: 'Huza',
    reportDescription: 'Tanga ikintu cyabuze cyangwa wasanze mu masegonda 30.',
    aiMatchDescription: 'AI yacu ishaka ibihuriye neza ku buryo bwikora.',
    connectDescription: 'Ganira mu mutekano kugira ngo ugarure ikintu.',
    
    // Contact Page
    contactTitle: 'Twandikire',
    contactDescription: 'Ufite ibibazo? Ukeneye ubufasha? Turi hano gukugufasha 24/7.',
    sendUsMessage: 'Twoherereze Ubutumwa',
    emailAddress: 'Aderesi ya Imeyili',
    subject: 'Ingingo',
    message: 'Ubutumwa',
    getInTouch: 'Twandikire',
    businessHours: 'Amasaha y\'Akazi',
    quickHelp: 'Ubufasha Bwihuse',
    
    // Footer
    quickLinks: 'Ihuza Ryihuse',
    support: 'Ubufasha',
    helpCenter: 'Ikigo cy\'Ubufasha',
    privacyPolicy: 'Politiki y\'Ibanga',
    termsOfService: 'Amabwiriza y\'Serivisi',
    poweredByAI: 'Bikoreshwa na AI',
    systemOnline: 'Sisitemu Ikora',
    madeWithLove: 'Byakozwe n\'urukundo rwa Rwanda',
    
    // Messages
    fillAllFields: 'Nyamuneka uzuza ibisabwa byose',
    itemReportedSuccess: 'Ikintu cyatanzwe neza!',
    trackingCode: 'Kode yo Gukurikirana',
    saveTrackingCode: 'Bika iyi kode kugira ngo ukurikirane ikintu cyawe.',
    messageSentSuccess: 'Ubutumwa bwoherejwe neza! Tuzagusubiza mu masaha 24.',
    
    // Placeholders
    enterFullName: 'Andika amazina yawe yose',
    enterPhoneNumber: '+250 788 123 456',
    enterItemTitle: 'urugero: Telefoni y\'iPhone 13 y\'umukara',
    enterDescription: 'Sobanura ikintu cyawe mu birambuye: ibara, ikigo cyakikoze, icyitegererezo, ibintu bidasanzwe, aho wabuzeyemo, n\'ibindi.',
    enterLocation: 'urugero: Isoko rya Kigali, Sitasiyo ya Nyabugogo',
    enterEmail: 'imeyili.yawe@urugero.com',
    enterSubject: 'Ni iki gishaka kuvuga?',
    enterMessage: 'Tubwire uko dushobora kugufasha...',
    
    // Tips
    tipsForBetter: 'Inama zo Kubona Ibisubizo Byiza',
    beSpecific: 'Ba musobanuri: Shyiramo ikigo cyakikoze, icyitegererezo, ibara, n\'ibintu bidasanzwe',
    mentionLocation: 'Vuga ibisobanuro by\'ahantu: Ahantu nyaha, ibimenyetso biri hafi',
    checkRegularly: 'Subiramo buri gihe: Ibintu bishya byasanzwe byongerwamo buri munsi',
    keepPhoneOn: 'Komeza telefoni yawe ikora: Tuzakumenyesha iyo habaye ibihuriye',
    
    // Image Upload
    uploadImage: 'Shyiramo Ifoto (Bitegetswe)',
    chooseImage: 'Hitamo Ifoto',
    imageHelp: 'Shyiramo ifoto kugira ngo AI ikugufashe gushaka',
    maxFileSize: 'Ubunini bwifoto: 5MB',
    supportedFormats: 'Byemewe: JPG, PNG, WEBP'
  }
};

// Translation function - reactive store
export const t = derived(currentLanguage, ($currentLanguage) => {
  return (key, params = {}) => {
    let translation = translations[$currentLanguage]?.[key] || translations.en[key] || key;
    
    // Replace parameters in translation
    Object.keys(params).forEach(param => {
      translation = translation.replace(`{${param}}`, params[param]);
    });
    
    return translation;
  };
});

// Language switching function
export function switchLanguage(lang) {
  currentLanguage.set(lang);
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem('language', lang);
  }
}

// Initialize language from localStorage
export function initLanguage() {
  if (typeof localStorage !== 'undefined') {
    const savedLang = localStorage.getItem('language');
    if (savedLang && translations[savedLang]) {
      currentLanguage.set(savedLang);
    }
  }
}