

function activeLinkPath(path) {
	let links = document.links;
	for (let i = 0; i < links.length; i++) {
		let href = links[i].getAttribute('href');
		if (href === path) {
			links[i].classList.add('active');
		}
	}
}



window.onload =  () => {
	activeLinkPath(window.location.pathname);

}

