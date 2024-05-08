/*
<nav>        
    <ul>            
        <li><a href="/">Home</a></li>
        <li><a href="#">Tecniche</a>
            <ul>
                <li><a href="/tecniche/impugnatura.html">Impugnatura</a></li>
                <li><a href="/tecniche/rotazione.html">Rotazione</a></li>
                <li><a href="/tecniche/colpi.html">Colpi</a></li>
                <li><a href="/tecniche/postura.html">Postura e Spostamenti</a></li>
                <li><a href="/tecniche/stili.html">Stili di Gioco</a></li>                    
            </ul>
        </li>
        <li><a href="#">Tennistavolo nel Mondo</a>
            <ul>
                <li><a href="/ping-pong/europa.html">In Europa</a></li>
                <li><a href="/ping-pong/italia.html">In Italia</a></li>
            </ul>
        </li>
        <li class="active"><a href="/chi-sono.html">Chi Sono</a></li>
    </ul>
</nav>
*/
let menu = 
    
        [
            { "title": "Home", "href": "/" },
            {
                "title": "Tecniche", "href": "#", "childs": [
                    { "title": "Impugnature", "href": "/tecniche/impugnatura.html" },
                    { "title": "Rotazione", "href": "/tecniche/rotazione.html" },
                    { "title": "Colpi", "href": "/tecniche/colpi.html" },
                    { "title": "Postura e Spostamenti", "href": "/tecniche/postura.html"},
                    { "title": "Stili di Gioco", "href": "/tecniche/stili.html" },
                ]
            },
            {
                "title": "Tennistavolo nel Mondo", "href": "#", "childs": [
                    { "title": "In Europa", "href": "/ping-pong/europa.html" },
                    { "title": "In Italia", "href": "/ping-pong/italia.html" },
                ]
            },
            { "title": "Chi Sono", "href": "/chi-sono.html" },
        ];


/**
 * Funzione ricorsiva per stampare menu dropdown
 * @param menu Array  
 * @param relative string 
 * @param ischild boolean 
 * @returns string
 */
function printMenu(menu, relative, ischild) {
    
    console.log(" - relative is: " + relative);

    let innerHtml='';
    if (Array.isArray(menu)) {
        for (let index = 0; index < menu.length; index++) {
            innerHtml += printMenu(menu[index], relative);
        }
    } else {
        if (menu["childs"] !== undefined) {        

            let hasTitle = (menu["title"] !== undefined);
            if (hasTitle) {
                let title = menu['title'];  
                innerHtml += '<li class="nav-item dropdown">';
                    
                innerHtml += '  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">' + title + '</a>';
                innerHtml += '  <ul class="dropdown-menu">';
                for (let index = 0; index < menu["childs"].length; index++) {
                    innerHtml += printMenu(menu["childs"][index], relative, true);
                }
                innerHtml += '  </ul>';            
                innerHtml += "</li>";
            } 
            
        } else {
            
            let title = menu['title'];
            let link = menu['href'];

            

            let active = false;
            if (link == relative) {
                active = true;
            }
            if (ischild) {
                innerHtml+='<li><a class="dropdown-item" href="' +link + '" onclick="return navigateTo(this)">' + title + '</a></li>';
            }
            else {
                classStr = '';
                if (active) {
                    classStr+= ' active';
                }
                innerHtml = '<li class="nav-item"><a class="nav-link'+classStr+'" href="' +link + '" onclick="return navigateTo(this)">' + title + '</a></li>';
            }
        }
    }
       
    return innerHtml;
}

$.when($.ready).then(function () {

    let relativeUrl = window.location.href;
    relativeUrl = "/"+relativeUrl.replace(/^(?:\/\/|[^/]+)*\//, '');
    console.log("Relative url: "+ relativeUrl);

    let htmlMenu = '<ul class="navbar-nav me-auto mb-2 mb-lg-0">';
    htmlMenu += printMenu(menu,relativeUrl,false);
    htmlMenu += '</ul>';
    $("#navbarSupportedContent").html(htmlMenu);
});

function navigateTo(o){
    let link = $(o).attr("href");
    if (link!=="/") {
        console.log("Will navigate to " + link);
        $.get(link, function(xhtml) {
            $("#dynamicpage").html(xhtml);
        });
        return false;
    }
}

