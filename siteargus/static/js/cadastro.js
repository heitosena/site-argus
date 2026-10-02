console.log("Hello, World!!")

const formularioLogin =document.getElementById("formCad")

const nome = document.getElementById("nome");
const email = document.getElementById("email");
const senha = document.getElementById("senha");
const confsenha = document.getElementById("confSenha");
const telefone = document.getElementById("telefone");

formCad.addEventListener("submit", function(event) {

    if (nome.value.lenght < 7){
        console.log("Digite seu nome completo");
        return;
    }

    if (senha != confSenha){
        console.log("As duas senhas devem ser iguais")
        return;
    }

   

});
