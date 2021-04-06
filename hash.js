document.addEventListener("DOMContentLoaded", function() {
    let dropZone = document.getElementById('drop_zone');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false)
      });
      
      function preventDefaults (e) {
        e.preventDefault()
        e.stopPropagation()
      }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false)
      });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false)
      });

    function highlight (e){
        dropZone.classList.add('highlight')
    }

    function unhighlight (e){
        dropZone.classList.remove('highlight')
    }
    // add handling for when files drop
    dropZone.addEventListener('drop', handleDrop, false)

    function handleDrop(e) {
        let dt = e.dataTransfer
        let files = dt.files
        
        handleFiles(files)
    }

    function handleFiles(files) {
        ([...files]).forEach(uploadFile)
      }
    
      function uploadFile(file) {
          let url = '/hash'
          let formData = new FormData()

          formData.append('file', file)

          fetch(url, {
            method: 'POST', 
            body: formData    
          })
          //the hash is in the
          .then(response => response.json())
          .then(result => {
            var hash = JSON.stringify(result);
            document.getElementById("error").innerHTML = hash;
            console.log('Success:', hash);
            
            
        })
          


          .catch(() => { alert("something went wrong") })
          
      }

});