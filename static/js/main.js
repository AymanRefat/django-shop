

function activeLinkPath(path) {
    let links = document.links;
    for (let i = 0; i < links.length; i++) {

        console.log(links[i].href);
        console.log(path);
        console.log(links[i].href === path ) ;

        if (links[i].pathname === path) {
            links[i].classList += ' active';
        }
    }
}



window.onload = function () {

    activeLinkPath(window.location.pathname);

}

