$(document).on("click", ".mainVideo", function () {
    var id = $(".mainVideo > img:nth-child(1)").data("id");
    get_url(id).done(function (data, status, xhr) {
        console.log(data)
        $(".mainVD").html(`<iframe class=\"mainVideo\" src=${data}></iframe>`)
    })
});
function get_url(id) {
    return $.ajax({
        url: "/find_url_by_id/" + id,
        method: "GET"
    })
}