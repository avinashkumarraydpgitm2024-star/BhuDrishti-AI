let baseUrl = config[0].Port.server.baseUrl;
let apiUrl = config[0].Port.server.apiUrl;
let resourceFolderUrl = config[0].Port.server.resourceFolderUrl;
let SuseApp = config[0].Layers.SuseApp.url;
let LfsApp = config[0].Layers.LfsApp.url;
let LandslideApp = config[0].Layers.LandslideApp.url;
// let ProjectRedirect = config[0].Port.ProjectRedirect.url;
let ProjectRedirect = config[0].Port.ProjectRedirect;

let landslideDash = config[0].Layers.Landslide_Dashboard.url;


async function fetchDataAndHandleErrors() {
    try {
        const response = await fetch(`${apiUrl}/News/datalist`);
        const mapLoader = document.getElementById('mapLoader');
        if (response.ok) {
            mapLoader.style.display = 'none';
        }
        else {
            document.getElementById("errormsg").classList.remove("d-none");
            mapLoader.style.display = 'none';
        }
    } catch (error) {
        console.error('Error:', error.message)
        mapLoader.style.display = 'none';
    }
}


fetchDataAndHandleErrors();


function openInNewTab(url) {
    let win = window.open(url, '_blank');
    win.focus();
}
// Function to open SuseApp URL in a new tab
function openInNewTabSuseApp() {
    openInNewTab(SuseApp);
}
function openInNewTabLfsApp() {
    openInNewTab(LfsApp);
}
function openInNewTabLandslideApp() {
    openInNewTab(landslideDash);
}

// ***************************  Recent Landslide Count Working code*******************************
const localStorageKey = 'landslideCount';
const fallbackCount = 33904;

function getStoredCount() {
    const storedValue = localStorage.getItem(localStorageKey)
    return storedValue !== null ? Number(storedValue) : fallbackCount
}

function setStoredCount(count) {
    localStorage.setItem(localStorageKey, count);
}

function updateLandslideCount(count) {
    document.getElementById('RecentlandslideCount').textContent = count;
}

async function fetchLandslideCount() {
    try {
        const response = await fetch(`${apiUrl}/Landslide/countGeojson`);
        const data = await response.json();
        console.log("data",data);
        if (response.ok && data.statusCode === 200) {
            const count = data.result[0].count;
            setStoredCount(count);
            updateLandslideCount(count);
        } else {
            // console.warn('API did not return success:', data.statusMessage);
            updateLandslideCount(getStoredCount());
        }
    } catch (error) {
        console.error('Error fetching data from API:', error);
        updateLandslideCount(getStoredCount());
    }
}

// Initialize the count on page load
document.addEventListener('DOMContentLoaded', () => {
    updateLandslideCount(getStoredCount());
    fetchLandslideCount();
});

// function redirectToProject() {
//     window.location.href = ProjectRedirect;
// }
function redirectToProject(type) {
    const urls = {
        meso: ProjectRedirect.mesoScaleUrl,
        macro: ProjectRedirect.macroScaleUrl,
        micro: ProjectRedirect.microScaleUrl,
        resourceanddevelopment:ProjectRedirect.ResearchAndDevelopment
    };
    if (urls[type]) {
        window.location.href = urls[type];
    }
}
