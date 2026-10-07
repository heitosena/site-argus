console.log("Hello, World!!");

const formularioCadastro = document.getElementById("formCad");

const nome = document.getElementById("nome");
const email = document.getElementById("email");
const senha = document.getElementById("senha");
const confsenha = document.getElementById("confSenha");
const telefone = document.getElementById("telefone");
const posicaoArroba = email.value.indexOf("@");
const posicaoPonto = email.value.indexOf(".", posicaoArroba);

formCad.addEventListener("submit", function (event) {
  event.preventDefault();

  //Validação do nome
  if (nome.value.length < 7) {
    console.log("Digite seu nome completo");
    return;
  }
  //validação da Senha
  if (senha.value != confSenha.value) {
    console.log("As duas senhas devem ser iguais");
    return;
  }
  if (senha.value.length < 8) {
    console.log("A senha deve ter no mínimo 8 caracteres");
    return;
  }
  //Validação do telefone
  telefone.addEventListener("input", function() {
    let valor = telefone.value.replace(/\D/g, "");

    if (valor.length > 11) {
        valor = valor.substring(0, 11);
    }

    if (valor.length > 6) {
        telefone.value = "(" + valor.substring(0, 2) + ") "
            + valor.substring(2, 7) + "-"
            + valor.substring(7);
    } 
    else if (valor.length > 2) {
        telefone.value = "(" + valor.substring(0, 2) + ") "
            + valor.substring(2);
    } 
    else {
        telefone.value = valor;
    }
});

  //validação do email
  if (posicaoArroba == -1 || posicaoPonto == -1) {
    console.log("Digite um email válido");
    return;
  }
});
