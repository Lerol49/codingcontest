var total_url_list = window.location.pathname.split("/");
var base_url = total_url_list[1];
total_url_list.splice(0, 1);

var url_with_href = "<a class=local_link href=/>home</a>";

for (i = 1; i < total_url_list.length; i++){  // loops through parts of the url, starting from
    var link = "";
    for (j = 0; j < i-1; j++){
        link += "/" + total_url_list[j];
    }

    url_with_href += "/" + "<a class=local_link href=" + "/" + base_url + link +">" + total_url_list[i - 1] + "</a>"
}
document.getElementById("directory").innerHTML = url_with_href

