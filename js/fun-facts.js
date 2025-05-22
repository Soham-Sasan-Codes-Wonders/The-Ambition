const funFacts = [
    "There are 24 letters in the Gayatri Mantra, and there are 24,000 Shlokas in the VALMIKI RAMAYANA. The first letter of every 1000th Shloka together of the Ramayana forms the Gayatri Mantra",
    "The unicorn is the national animal of Scotland",
    "Octopuses have three hearts",
    "Honey never spoils",
    "A banana is botanically a berry, but a strawberry is not",
    "Sharks have existed longer than trees",
    "Cleopatra lived closer in time to the Moon landing than to the building of the Great Pyramid",
    "Oxford University is older than the Aztec Empire",
    "Saudi Arabia imports camels from Australia",
    "Einstein did not fail mathematics as a child",
    "Lightning often strikes the same place twice",
    "Wombats poop in cubes",
    "The “immortal jellyfish” can revert its age",
    "France was still executing people by guillotine when Star Wars came out",
    "North Korea and Finland are separated by only one country",
    "Anne Frank and Martin Luther King Jr. were born in the same year",
    "The shortest war in recorded history lasted only 38 - 45 minutes",
    "Mickey Mouse and Minnie Mouse got married in real life (in a way)",
    "The major fear of Walt Disney was mice",
    "Sea otters hold hands while sleeping",
    "The voice of a blue whale heart can be heard two miles away"
];

var currentFunFact = ""; 

function selectAndStoreFunFact() {
    if (funFacts.length > 0) {
        const randomIndex = Math.floor(Math.random() * funFacts.length);
        currentFunFact = funFacts[randomIndex];
    } else {
        currentFunFact = "No fun facts available at the moment!";
        console.warn("Fun fact list is empty in fun-facts.js.");
    }
}
function displayFunFactStaticallyOnPage() {
    const funFactSectionElement = document.getElementById('funFactSection');
    const funFactTextElement = document.getElementById('funFactText');
    const funFactTitleElement = funFactSectionElement ? funFactSectionElement.querySelector('h3') : null;

    if (!funFactSectionElement || !funFactTextElement) return;
    if (!currentFunFact) selectAndStoreFunFact();

    funFactSectionElement.style.visibility = 'visible';
    if (funFactTitleElement && !funFactTitleElement.classList.contains('matrix-text')) funFactTitleElement.classList.add('matrix-text');
    funFactTextElement.textContent = currentFunFact;
    if (!funFactTextElement.classList.contains('matrix-text')) funFactTextElement.classList.add('matrix-text');
}