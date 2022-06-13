

function activeLinkPath(path) {
	let links = document.links;
	for (let i = 0; i < links.length; i++) {
		if (links[i].pathname === path) {
			links[i].classList.add('active');
		}
	}
}



window.onload =  () => {
	
	activeLinkPath(window.location.pathname);

}

