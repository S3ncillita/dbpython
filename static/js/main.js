
console.log("El script main.js se ha cargado correctamente.");

const btnDelete=document.querySelectorAll('.btn-delete')

if(btnDelete){
    const btnArray=Array.from(btnDelete);
    btnArray.forEach((btn) =>{
        btn.addEventListener('click',(e)=>{
            if(!confirm('Desea eliminar lo seleccionado?')){
                e.preventDefault();
            }

        });
    });
}