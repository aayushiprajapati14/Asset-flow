let editAssetId = null;
let assets=[

{
id:"AST001",
name:"Dell Laptop",
category:"Electronics",
status:"Available",
allocated:"-"
},

{
id:"AST002",
name:"HP Laptop",
category:"Electronics",
status:"Allocated",
allocated:"Rahul Sharma"
},

{
id:"AST003",
name:"Office Chair",
category:"Furniture",
status:"Under Maintenance",
allocated:"-"
}

];

let assetEditIndex=-1;

function loadAssets(){

let tbody=document.getElementById("assetTable");
//Find <tbody id="assetTable">.

tbody.innerHTML="";

assets.forEach((a,index)=>{

let color="success";//by default, status is success

if(a.status=="Allocated") color="primary";

if(a.status=="Under Maintenance") color="warning";

if(a.status=="Lost") color="danger";

if(a.status=="Retired") color="secondary";
////means we are adding a new row to the table for each asset while the old one remains there. We are not replacing the old one.` means we are accesing html
 
tbody.innerHTML+=` 
 
<!--badge is a Bootstrap class that makes the status look like a small pill/badge.
<tr>

<td>${a.id}</td>

<td>${a.name}</td>

<td>${a.category}</td>

<td>

<span class="badge bg-${color}">  <!-bg-${color} changes depending on the status.-->

${a.status}

</span>

</td>

<td>${a.allocated}</td>

<td>

<button
class="btn btn-warning btn-sm"
onclick="editAsset(${index})">

<i class="fa fa-edit"></i>

</button>

<button
class="btn btn-danger btn-sm"
onclick="deleteAsset(${index})">

<i class="fa fa-trash"></i>
<!--button → creates a button.
btn → Bootstrap button.
btn-warning → yellow Bootstrap button.
btn-sm → small button.
Then:
onclick="editAsset(${index})"
means:
When this button is clicked, call editAsset() and give it this asset's index.-->

</button>

</td>

</tr>

`;

});

}
function searchAsset(){ 
    let input = document.getElementById("assetSearch");
    let filter = input.value.toLowerCase();
    let rows = document.querySelectorAll("#assetTable tr");//searching evry column and row
    rows.forEach(row => {
        let text = row.innerText.toLowerCase();
        if (text.includes(filter)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}
async function editAsset(assetId) { //async means this function is going to take some time to complete, and we want to wait for it to finish before moving on to the next line of code.

    editAssetId = assetId;
    document.getElementById("assetForm").action = "/update_asset/" + assetId;//what happens is we are selecting the form and when we click on edit button, we are changing the action of the form to update_asset/assetId. So when we submit the form, it will go to the update_asset route with the assetId.
    document.getElementById("addAssetButton").textContent = "Edit Asset";
    let response = await fetch("/get_asset/" + assetId);//fetch is js ways to make a request to the server. await means we want to wait for the response before moving on to the next line of code.
//response of flask is stored in response variable. await means we want to wait for the response before moving on to the next line of code.
    let asset = await response.json();//our flask route returns a dictionary flask send it to browser as a json object
    document.getElementById("assetName").value = asset.name;
    document.getElementById("assetCategory").value = asset.category;
    document.getElementById("assetStatus").value = asset.status;
    document.getElementById("allocatedTo").value = asset.allocated;

    let modal = new bootstrap.Modal(
        document.getElementById("assetModal")
    );

    modal.show();
}
function deleteAsset(assetId) {

    let confirmDelete = confirm("Are you sure you want to delete this asset?");

    if (confirmDelete) {
        window.location.href = "/delete_asset/" + assetId;
    }
}
function clearAssetForm() {

    document.getElementById("assetForm").action = "/add_asset";//to bring it back to the add_asset route when we click on the add asset button after editing an asset. So when we submit the form, it will go to the add_asset route.
    editAssetId = null;
    document.getElementById("addAssetButton").textContent = "Register Asset";


    // your existing code for clearing the fields...
}
//window.onload=loadAssets;