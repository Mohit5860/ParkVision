function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



document.getElementById("scan").addEventListener("click", () => {
    console.log("test");
                fetch("http://127.0.0.1:8000/scan", {method: "POST",
            headers: {
        'X-CSRFToken': getCookie('csrftoken'),}
            })
                .then(response => response.json())
                .then(data => document.getElementById("scaned").innerHTML= `<img src="${data.image_url}" />  <p> ${data.number}</p> <input type="hidden" name="number" value="${data.number}" />`)
            })

            document.getElementById("generate").addEventListener("click", () => {
                var generateUrl = "http://127.0.0.1:8000/generate";
                fetch(generateUrl, {method: "POST", 
                headers: {
        'X-CSRFToken': getCookie('csrftoken'), // Include the CSRF token in the headers
    },
            })
                .then(response => response.json())
                .then(data => {
                    const listHtml = data.my_list.map(item => {
                        return `<label>
                                <input type="checkbox" name="mycheckbox" value="${item}" />
                                <p>${item}</p>
                            </label>`
                    }).join('');
                    document.getElementById("generated").innerHTML = listHtml;
                    const checkboxes = document.querySelectorAll('input[name="mycheckbox"]');
checkboxes.forEach(checkbox => {
    checkbox.addEventListener("change", () => {
        if (checkbox.checked) {
            checkboxes.forEach(other => {
                if (other !== checkbox) {
                    other.checked = false;
                    console.log("Other checkbox unchecked");
                }
            });
        }
    });
});
                })
                
            })
