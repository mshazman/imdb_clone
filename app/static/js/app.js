export_button.addEventListener("click", task)
var movie_id = document.getElementById('export_button').getAttribute('value')
extract_url= 'http://127.0.0.1:5000/extract/'+ movie_id;
function task() {
    console.log(extract_url)
    fetch(extract_url).
        then(res => res.json()).
        then(data =>{
            document.getElementById('export_button').name = data.id
            return data.id
    }).
        then(task_id => {
            send(task_id);
    })
}

function send(task_id){
    status_url = 'http://127.0.0.1:5000/task/status/' + task_id
    console.log(status_url)
    link = 'http://127.0.0.1:5000/task/result/' + task_id
    download_link ='window.location.href=' + '"'+ 'http://127.0.0.1:5000/task/result/' + task_id + '"'
    $.ajax({
        type: "get",
        url: status_url,
        success:function(data)
        {
            //console.log the response
            console.log(data)
            console.log(data.state)
            if (data.state == 'PENDING')
            {
                debugger;
                document.getElementById('export_button').innerHTML = 'Starting'
                document.getElementById('export_button').setAttribute('disabled', true)
            }
            else if(data.state=='PROGRESS')
            {
                document.getElementById('export_button').innerHTML = 'Exporting: ' + data.progress.toString()
                document.getElementById('export_button').setAttribute('disabled', true)
            }
            else if (data.state=='SUCCESS')
            {
                window.location = link
                document.getElementById('export_button').innerHTML = 'Download'
                document.getElementById('export_button').disabled = false
                document.getElementById('export_button').setAttribute('onclick', download_link)
                clearTimeout(timerid)

            }

         let timerid=   setTimeout(function(){
                send(task_id);
            }, 5000);
        }
    });
}
