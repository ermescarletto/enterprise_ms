  const toggleSidebar = document.getElementById('toggleSidebar');
    const closeSidebar = document.getElementById('closeSidebar');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    // Open Sidebar
    toggleSidebar.addEventListener('click', () => {
      sidebar.classList.add('show');
      overlay.classList.add('show');
    });

    // Close Sidebar
    closeSidebar.addEventListener('click', () => {
      sidebar.classList.remove('show');
      overlay.classList.remove('show');
    });

    // Close Sidebar by clicking on the overlay
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('show');
      overlay.classList.remove('show');
    });

    // Toggle Mini Sidebar (collapsed state)
    sidebar.addEventListener('transitionend', () => {
      if (!sidebar.classList.contains('show') && !sidebar.classList.contains('mini')) {
        sidebar.classList.add('mini');
      } else if (sidebar.classList.contains('show')) {
        sidebar.classList.remove('mini');
      }
    });



    //FUNCOES DO CPF


function aplicarMascaraCPF(campo) {
    campo.addEventListener("input", function() {
        let valor = campo.value.replace(/\D/g, '');  // Remove tudo que não é número
        if (valor.length <= 11) {
            valor = valor.replace(/(\d{3})(\d{3})(\d{3})(\d{1})/, '$1.$2.$3-$4');  // Máscara CPF
        }
        campo.value = valor;
    });
}

// Função para validar CPF
function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');  // Remove qualquer coisa que não seja número

    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) {
        return false;  // Verifica se o CPF é inválido (ex: 111.111.111-11)
    }

    // Valida o primeiro dígito verificador
    let soma = 0;
    let peso = 10;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf[i]) * peso--;
    }
    let resto = soma % 11;
    if (resto < 2) {
        if (parseInt(cpf[9]) !== 0) return false;
    } else {
        if (parseInt(cpf[9]) !== 11 - resto) return false;
    }

    // Valida o segundo dígito verificador
    soma = 0;
    peso = 11;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf[i]) * peso--;
    }
    resto = soma % 11;
    if (resto < 2) {
        if (parseInt(cpf[10]) !== 0) return false;
    } else {
        if (parseInt(cpf[10]) !== 11 - resto) return false;
    }

    return true;
}