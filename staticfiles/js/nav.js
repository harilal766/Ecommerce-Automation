function html_injector(element_id,content){
    const html_element = document.getElementById(element_id);
    if (html_element) {
        html_element.innerHTML = content;
    }
}




function navbar() {
    const navbar_links = {
        "Home" : "www.google.com",
        "About us" : "/about"
    }
    const nav = Object.keys(navbar_links);
    navbar_links_length = navbar_links.length;

    let nav_code = `<nav> <ul>`;

    for (let i = 0; i<navbar_links_length; i++) {
        var list = `<li class="nav-item"><a class="nav-link" href="${navbar_links[i]}">${i}</a></li>`;
        nav_code += list;
    }
    nav_code += "</ul></nav>";

    //return nav_code;
    console.log(nav_code);
    const html_footer = document.getElementById("navigation");
    if (html_footer) {
        html_footer.innerHTML = nav_code;
    }
}

navbar();
