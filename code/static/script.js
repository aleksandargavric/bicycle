function uploadPMFiles() {
  uploadFiles("Input", true);

}

function uploadRefFiles() {
  uploadFiles("References", false);

}

function uploadFiles(selection, extendedModalities) {
  event.preventDefault();
  if(labels.length == 0) {
      alert("Please create non-empty set of domain features.")
      return;
  }
  const imageFiles = document.getElementById('image'+selection).files;
  const txtFiles = document.getElementById('txt'+selection).files;
  let allFiles = [];
  let processedImageCount = 0;

  // Resize and collect image files
  Array.from(imageFiles).forEach(file => {
      if (file.type.startsWith('image/')) {
          resizeImage(file, 200, 100, (resizedBlob) => {
              allFiles.push({blob: resizedBlob, name: 'resized_' + file.name});
              processedImageCount++;
              checkAllFilesProcessed();
          });
      }
  });

   // Directly add txt files
  allFiles = allFiles.concat(Array.from(txtFiles).map(file => ({blob: file, name: file.name})));
  
  if (extendedModalities) {
  // More modalities
  const audioFiles = document.getElementById('audio'+selection).files;
  const videoFiles = document.getElementById('video'+selection).files;
  allFiles = allFiles.concat(Array.from(audioFiles).map(file => ({blob: file, name: file.name})));
  allFiles = allFiles.concat(Array.from(videoFiles).map(file => ({blob: file, name: file.name})));
  }

  function checkAllFilesProcessed() {
      if (processedImageCount === imageFiles.length) {
          if(extendedModalities)
          {
              sendPMFilesToServer(allFiles);
          }
          else
          {
              sendRefFilesToServer(allFiles);
          }

      }
  }
  // Call immediately in case there are no images
  if(imageFiles.length === 0) checkAllFilesProcessed();
}

function visualizeFile(filePath) {
 // Check file type and create corresponding HTML element
const fileType = getFileType(filePath);
let fileElement;
if (fileType === 'image') {
  fileElement = document.createElement('img');
  fileElement.src = filePath;
} else if (fileType === 'audio') {
  fileElement = document.createElement('audio');
  fileElement.controls = true;
  fileElement.src = filePath;
} else if (fileType === 'video') {
  fileElement = document.createElement('video');
  fileElement.controls = true;
  fileElement.src = filePath;
} else if (fileType === 'text') {
  fileElement = document.createElement('textarea');
  fileElement.readOnly = true;
  // Fetch the text content of the file
  fetch(filePath)
    .then(response => response.text())
    .then(text => fileElement.textContent = text)
    .catch(error => console.error('Error fetching text file:', error));
}
// Append the file element to the visualization div
return fileElement;
}

function getFileType(filePath) {
const extension = filePath.split('.').pop().toLowerCase();
if (extension === 'jpg' || extension === 'jpeg' || extension === 'png' || extension === 'gif') {
  return 'image';
} else if (extension === 'mp3' || extension === 'wav' || extension === 'ogg') {
  return 'audio';
} else if (extension === 'mp4' || extension === 'webm' || extension === 'ogg') {
  return 'video';
} else if (extension === 'txt') {
  return 'text';
} else {
  return 'unsupported';
}
}

function sendPMFilesToServer(files) {
  const formData = new FormData();

  const fallbackDateInput = document.getElementById('fallbackDateTime').value; // Get the fallback date value
// Convert the fallback date to an ISO string, or use a default value if not set
  let fallbackDateString = fallbackDateInput ? new Date(fallbackDateInput).toISOString() : new Date().toISOString();
  
 const textInput = document.getElementById('textInput').value;
 if(textInput) {
 formData.append('textModality', textInput); 
 formData.append(`date_0`, fallbackDateString); 
 }

  for (let i = 0; i < files.length; i++) {
      formData.append('files[]', files[i].blob, files[i].name);

      // Safely attempt to convert lastModified to a Date object
      try {
          let lastModifiedDate = new Date(files[i].lastModified);
          if (isNaN(lastModifiedDate.getTime())) {
              throw Error("Invalid date");
          }
          let dateString = lastModifiedDate.toISOString(); // Convert to ISO string
          formData.append(`date_${i}`, dateString);
      } catch (error) {
         formData.append(`date_${i}`, fallbackDateString);    
      }
  }

  // console.log(formData);
  const tableContainer = document.getElementById('table-container');
  tableContainer.innerHTML = 'Processing the input data... ';
  tableContainer.appendChild(getLoading());

  fetch('/upload-pm', {
      method: 'POST',
      body: formData,
  })
  .then(response => response.json())
  .then(data => {
      displayResults(data, tableContainer);
  })
  .catch(error => console.error('Error:', error));
}

function displayResults(data, tableContainer) {
  console.log(data);
  tableContainer.innerHTML = ''; // Clear previous content
  const title = document.createElement('h2');
title.innerHTML = "Created event logs ("+ data.request_id +")<br>";
  tableContainer.appendChild(title);
  tableContainer.appendChild(document.createElement('br'));

  // Function to create and append rows to the table
  const appendPMRows = (data, tbody, indent = 0) => {
      data.forEach(item => {
          const tr = document.createElement('tr');

          const tdFile = document.createElement('td');
          const tdFilePreview = document.createElement('td');
          // Apply indentation for nested items
          tdFile.style.paddingLeft = `${indent}px`;
          tdFile.textContent = item.filename;
          const tdResult = document.createElement('td');
          const tdAnalysis = document.createElement('td');
          const tdTimeStart = document.createElement('td');
          const tdTimeEnd = document.createElement('td');
          const tdCaseId = document.createElement('td');
          const tdReferences = document.createElement('td');

          let fileElement = visualizeFile('/static/uploads/'+ item.filename); 
          tdFilePreview.appendChild(fileElement); 

        if (item.caseid) {
            tdCaseId.textContent = item.caseid;
          }
          if (item.message) {
              tdResult.textContent = item.message;
          } 
          if (item.timestamp_start) {
              tdTimeStart.textContent = item.timestamp_start;
          } 
          if (item.timestamp_end) {
              tdTimeEnd.textContent = item.timestamp_end;
          } 

          // Check for and process any chunks recursively
          if (item.chunks) {
              item.chunks.forEach(chunk => {
                 appendPMRows([chunk], tbody, indent + 15); // Increase indentation for nested items
              });
          }

          if (item.analysis) {
              tdAnalysis.textContent = "Computing modality instance [" + item.analysis + "]...";
              // Append the image to the container
              tdAnalysis.appendChild(getLoading());
              tdAnalysis.id = item.analysis;
          }

          tr.appendChild(tdFilePreview);
          tr.appendChild(tdTimeStart);
          tr.appendChild(tdTimeEnd);
          tr.appendChild(tdCaseId);
          tr.appendChild(tdResult);
          tr.appendChild(tdFile);
          tr.appendChild(tdAnalysis);
          tr.appendChild(tdReferences);
          if (item.analysis) {
              labels.forEach(itemLabel => {
                  const tdAnalysisItem = document.createElement('td');
                  tdAnalysisItem.textContent = "Matching with " + itemLabel +"... ";
                  // Append the image to the container
                  tdAnalysisItem.appendChild(getLoading());
                  tdAnalysisItem.id = item.analysis + itemLabel;
                  tr.appendChild(tdAnalysisItem);
              });
          }
          tbody.appendChild(tr);
      });
  };

  // Check if data is not empty
  if (data && data.results && data.results.length > 0) {
      
      const table = document.createElement('table');
      table.classList.add('table');

      // Create table header
      const thead = document.createElement('thead');
      const trHead = document.createElement('tr');

      const thFilePreview = document.createElement('th');
      thFilePreview.textContent = 'Input preview';
      const thT1 = document.createElement('th');
      thT1.textContent = 'Timestamp Start';
      const thT2 = document.createElement('th');
      thT2.textContent = 'Timestamp End';
      const thCaseID = document.createElement('th');
      thCaseID.textContent = 'Case Id';
      const thResult = document.createElement('th');
      thResult.textContent = 'Status';
      const thFile = document.createElement('th');
      thFile.textContent = 'Reference file';
      const thAnalysis = document.createElement('th')
      thAnalysis.textContent = 'Analysis';
      const thReferences = document.createElement('th')
      thReferences.textContent = 'Reference matches';
      
      trHead.appendChild(thFilePreview);
      trHead.appendChild(thT1);
      trHead.appendChild(thT2);
      trHead.appendChild(thCaseID);
      trHead.appendChild(thResult);
      trHead.appendChild(thFile);
      trHead.appendChild(thAnalysis);
      trHead.appendChild(thReferences);
      labels.forEach(itemLabel => {
          const thAnalysisItem = document.createElement('th');
          thAnalysisItem.textContent = "Match: " + itemLabel;
          trHead.appendChild(thAnalysisItem);
      });
      thead.appendChild(trHead);
      table.appendChild(thead);

      // Create table body
      const tbody = document.createElement('tbody');
      appendPMRows(data.results, tbody); // Use the new appendRows function here
      table.appendChild(tbody);

      tableContainer.appendChild(table);
      const download = document.createElement('div');
    download.innerHTML = "<p> Download link: <a href='" + data.csv + "'>" + data.csv + "</a> (Computing is still in progress) </p>";
      tableContainer.appendChild(document.createElement('br')); // Add line break for spacing


// Create a Bootstrap button element
      const downloadButton = document.createElement('a');
      downloadButton.setAttribute('href', data.csv);
      downloadButton.setAttribute('class', 'btn btn-primary btn-sm'); // Bootstrap button classes for large primary button
      downloadButton.setAttribute('role', 'button');
      downloadButton.textContent = 'Download data as CSV'; // Text content for the button

     // Append the button to the table container
     tableContainer.appendChild(download);
     tableContainer.appendChild(document.createElement('br')); // Add line break for spacing
     tableContainer.appendChild(downloadButton);
     tableContainer.appendChild(document.createElement('br'));
     tableContainer.appendChild(document.createElement('br'));
     tableContainer.appendChild(document.createElement('br'));

     let txt_paths = data.txt_paths;
     let image_paths = data.image_paths;
     let audio_paths = data.audio_paths;
     let request_id = data.request_id;
     let csvpath = data.csv;

     const formData = new FormData();
     formData.append('txt_paths', txt_paths)
     formData.append('image_paths', image_paths)
     formData.append('audio_paths', audio_paths)
     formData.append('request_id', request_id)
     formData.append('csv', csvpath)
     formData.append('labels', labels)

     fetch('/compute-event-log', {
          method: 'POST',
          body: formData,
      })
      .then(response => response.json())
      .then(modalities => {
          console.log(modalities);
          downloadButton.setAttribute('href', modalities.csv);
          download.innerHTML = "<p> Download link [computing finished]: <a href='" + modalities.csv + "'>" + modalities.csv + "</a> </p>";
          downloadButton.textContent = 'Download Event Log';
          modalities.results.forEach(item => {
              // Analysis td
              const tdAnalysis = document.getElementById(item.id);
              tdAnalysis.textContent = "Top 3 domain matches: ";
              
              // Sorting the result keys by value
              const sortedResults = Object.entries(item.result).sort((a, b) => b[1] - a[1]);
              
              // Selecting only the top 3 entries
              const top3 = sortedResults.slice(0, 3);

              const resultList = document.createElement('ul');
              top3.forEach(([key, value]) => {
                  const li = document.createElement('li');
                  li.textContent = `${key}: ${value.toFixed(2)}`;
                  resultList.appendChild(li);
              });
              
              tdAnalysis.appendChild(resultList);

              // Classes tds
              Object.entries(item.result).forEach(([key, value]) => {
                  const tdAnalysisClass = document.getElementById(item.id + key);
                  tdAnalysisClass.textContent = `${key}: ${value.toFixed(2)}`;
              });
          });
          alert("Event log computation finished.");
      })
      .catch(error => console.error('Error:', error));


  } else {
      // In case of no data or empty response
      tableContainer.textContent = 'No files processed or an error occurred.';
  }

}

function resizeImage(file, maxWidth, maxHeight, callback) {
  const reader = new FileReader();
  reader.onload = function(event) {
      const img = new Image();
      img.onload = function() {
          let width = img.width;
          let height = img.height;

          if (width > height) {
              if (width > maxWidth) {
                  height *= maxWidth / width;
                  width = maxWidth;
              }
          } else {
              if (height > maxHeight) {
                  width *= maxHeight / height;
                  height = maxHeight;
              }
          }

          const canvas = document.createElement('canvas');
          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, width, height);
          canvas.toBlob(callback, file.type);
      };
      img.src = event.target.result;
  };
  reader.readAsDataURL(file);
}
var labels = [];
var customLabels = [];

function getLoading(){
  let loading = document.createElement('img');
  // Set the source of the image to your loading.gif file
  loading.src = '/static/loading.gif';
  // Set the size of the image
  loading.width = 20;
  loading.height = 20;    
  return loading;
}
          

function updateLabels(newLabel) {
if (!labels.includes(newLabel)) {
  labels.push(newLabel);
}
}

function removeLabel(label) {
var index = labels.indexOf(label);
if (index !== -1) {
  labels.splice(index, 1);
}
}

function addTodoItem(newTodo) {
var todoList = document.getElementById('todo-list');

if (newTodo && labels.indexOf(newTodo) == -1) {
  updateLabels(newTodo);
  
  var listItem = document.createElement('li');
  listItem.classList.add('list-group-item');

  var textSpan = document.createElement('span');
  textSpan.textContent = newTodo;
  listItem.appendChild(textSpan);

  var deleteButton = document.createElement('button');
  deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
  deleteButton.classList.add('btn', 'btn-danger', 'btn-sm', 'float-right');
  deleteButton.onclick = function() { 
    removeLabel(newTodo);
    deleteTodoItem(listItem); 
  };
  listItem.appendChild(deleteButton);

  var editButton = document.createElement('button');
  editButton.innerHTML = '<i class="fas fa-edit"></i>';
  editButton.classList.add('btn', 'btn-info', 'btn-sm', 'float-right', 'mr-2');
  editButton.onclick = function() { editTodoItem(textSpan, listItem); };
  listItem.appendChild(editButton);

  todoList.appendChild(listItem);
} else {
  alert('Please enter a non blank and unique item.');
}
}

function deleteTodoItem(item) {
if (confirm('Are you sure you want to delete this item?')) {
  item.remove();
}
}

function editTodoItem(textSpan, listItem) {
var oldValue = textSpan.textContent;
var newText = prompt('Edit your item:', oldValue);
if (newText !== null && newText.trim() !== '' && labels.indexOf(newText.trim()) == -1) {
  var newValue = newText.trim();
  textSpan.textContent = newValue;
  removeLabel(oldValue);
  listItem.remove();
  addTodoItem(newValue);
}
}

document.getElementById('button-add-todo').addEventListener('click', function() {
var todoInput = document.getElementById('todo-input');
var newTodo = todoInput.value.trim();
addTodoItem(newTodo);
todoInput.value = ''; // Clear the input after adding
});

document.getElementById('todo-input').addEventListener('keypress', function(e) {
if (e.key === 'Enter') {
  var todoInput = document.getElementById('todo-input');
  var newTodo = todoInput.value.trim();
  addTodoItem(newTodo);
  todoInput.value = ''; // Clear the input after adding
}
});

var previousDomainValue = null;

document.querySelectorAll('input[name="preset"]').forEach(function(input) {
input.addEventListener('change', function(e) {
  var selectedValue = e.target.value;
  var presetLists = {
    'dna': ['unboxing', 'filling tube by spitting', 'replacing caps', 'shaking tube', 'checking tube', 'sealing biohazard bag', 'placing tube into biohazard bag'],
    'ikea': ['no action', 'unboxing', 'drilling', 'aligning parts', 'reading printed user manual', 'screwing', 'fitting components together', 'tightening bolts and screws', 'attaching hardware', 'adjusting hinges and sliders', 'securing joints', 'assembling drawers and shelves', 'installing legs or wheels', 'mounting brackets', 'positioning back panels', 'fastening dowels', 'testing stability and functionality'],
    'dnaikea': ['adjusting hinges and sliders', 'aligning parts', 'assembling drawers and shelves', 'attaching hardware', 'checking tube', 'drilling', 'fastening dowels', 'filling tube by spitting', 'fitting components together', 'installing legs or wheels', 'mounting brackets', 'no action', 'placing tube into biohazard bag', 'positioning back panels', 'reading printed user manual', 'replacing caps', 'securing joints', 'sealing biohazard bag', 'screwing', 'shaking tube', 'testing stability and functionality', 'tightening bolts and screws', 'unboxing']
  };
  
  document.getElementById('todo-list').innerHTML = '';    
    if (selectedValue !== 'clear') {
      if(previousDomainValue === 'clear')
          customLabels = labels;
      labels = [];
      var selectedList = presetLists[selectedValue];
      selectedList.forEach(function(item) {
          addTodoItem(item);  
      
      });
  }else {
      labels = [];
      if(customLabels.length != 0) {
      var selectedList = customLabels;
      selectedList.forEach(function(item) {
          addTodoItem(item);     
    });
  }
    customLabels = [];
  }
  previousDomainValue = selectedValue;
  console.log(labels);
  console.log(customLabels);
});
});

document.querySelectorAll('.custom-file-input').forEach(function(input) {
  input.addEventListener('change', function(e) {
    var label = e.target.nextElementSibling;
    var files = e.target.files;
    if (files.length === 1) {
      label.innerHTML = files[0].name + ' ' + e.target.name + ' inputs selected';
    } else {
      label.innerHTML = files.length + ' ' + e.target.name + ' inputs selected';
    }
  });
});

function sendRefFilesToServer(files) {
  const formData = new FormData();
  const textInput = document.getElementById('textReferences').value;
  if(textInput) {
      formData.append('textModality', textInput); 
  }

  for (let i = 0; i < files.length; i++) {
      formData.append('files[]', files[i].blob, files[i].name);
  }

  formData.append('labels', labels)

  const tableContainer = document.getElementById('table-container');
  tableContainer.innerHTML = 'Processing the reference data... ';
  tableContainer.appendChild(getLoading());

  fetch('/upload-ref', {
      method: 'POST',
      body: formData,
  })
  .then(response => response.json())
  .then(data => {
      displayDomainInf(data, tableContainer);
  })
  .catch(error => console.error('Error:', error));
}

function displayDomainInf(data, tableContainer) {
  console.log(data);
  tableContainer.innerHTML = ''; // Clear previous content
  const title = document.createElement('h2');
title.innerHTML = "Domain inferring results("+ data.request_id +")<br>";
  tableContainer.appendChild(title);
  tableContainer.appendChild(document.createElement('br'));

  // Function to create and append rows to the table
  const appendRefRows = (data, tbody) => {
      data.forEach(item => {
          const tr = document.createElement('tr');
          const tdFilePreview = document.createElement('td');
          const tdAnalysis = document.createElement('td');
          const imagePath = '/static/uploads/'+ item.filename;
          let fileElement = visualizeFile(imagePath); 
          tdFilePreview.appendChild(fileElement); 

          if (item.analysis) {
              tdAnalysis.textContent = "Response [" + item.analysis + "]:";
              tdAnalysis.appendChild(document.createElement('br'));
              var textareatdAnalysis = document.createElement('textarea');
              textareatdAnalysis.id = item.analysis;
              textareatdAnalysis.style.width = '100%';
              textareatdAnalysis.style.height = '100%';
              tdAnalysis.appendChild(textareatdAnalysis);
              fetchLLM(imagePath, item.analysis);
          }

          tr.appendChild(tdFilePreview);
          tr.appendChild(tdAnalysis);
          // if (item.analysis) {
          //     labels.forEach(itemLabel => {
          //         const tdAnalysisItem = document.createElement('td');
          //         tdAnalysisItem.textContent = "Response " + itemLabel +"... ";
          //         // Append the image to the container
          //         tdAnalysisItem.appendChild(getLoading());
          //         tdAnalysisItem.id = item.analysis + itemLabel;
          //         tr.appendChild(tdAnalysisItem);
          //     });
          // }
          tbody.appendChild(tr);
      });
  };

  // Check if data is not empty
  if (data && data.results && data.results.length > 0) {
      const table = document.createElement('table');
      table.classList.add('table');

      // Create table header
      const thead = document.createElement('thead');
      const trHead = document.createElement('tr');

      const thFilePreview = document.createElement('th');
      thFilePreview.textContent = 'Input preview';
      const thAnalysis = document.createElement('th')
      thAnalysis.textContent = 'Domain analysis';
      
      trHead.appendChild(thFilePreview);
      trHead.appendChild(thAnalysis);
      // labels.forEach(itemLabel => {
      //     const thAnalysisItem = document.createElement('th');
      //     thAnalysisItem.textContent = "Domain feature: " + itemLabel;
      //     trHead.appendChild(thAnalysisItem);
      // });
      thead.appendChild(trHead);
      table.appendChild(thead);

      // Create table body
      const tbody = document.createElement('tbody');
      appendRefRows(data.results, tbody);
      table.appendChild(tbody);

      tableContainer.appendChild(table);
      tableContainer.appendChild(document.createElement('br')); // Add line break for spacing
     tableContainer.appendChild(document.createElement('br'));
     tableContainer.appendChild(document.createElement('br'));

  } else {
      // In case of no data or empty response
      tableContainer.textContent = 'No input processed or an error occurred.';
  }

}

async function fetchLLM(filePath, elementId) {
  const url = '/stream-llm';
  const postData = {
      file: filePath,
      labels: labels.toString(),
  };
  const response = await fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json' // Adjust content type as needed
      },
      body: JSON.stringify(postData)
  });
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  document.getElementById(elementId).textContent = '';

  while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const text = decoder.decode(value, {stream: true});
      console.log(text);
      document.getElementById(elementId).textContent += `${text}`;
  }
  console.log('Stream for '+ elementId + ' finished.');
}