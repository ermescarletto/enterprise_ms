document.addEventListener("DOMContentLoaded", function () {
        var toastElements = document.querySelectorAll(".messages");
        toastElements.forEach(function (toastEl) {
            var toast = new bootstrap.Toast(toastEl);
            toast.show();
        });
 });

//modais
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
};

document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("modal"); // Substitua pelo ID real do seu modal
    modal.addEventListener("shown.bs.modal", function () {

        const addBtn = document.getElementById("add");
        const removeBtn = document.getElementById("remove");
        const available_options = document.getElementById("available");
        const selected_options = document.getElementById("selected");
        const selectAllLeft = document.getElementById("select-all-left");
        const selectAllRight = document.getElementById("select-all-right");

        addBtn?.addEventListener("click", function () {
            moveSelectedOptions(available_options, selected_options);
            console.log('addBtn');
        });

        removeBtn?.addEventListener("click", function () {
            moveSelectedOptions(selected_options, available_options);
            console.log('removeBtn');
        });

        selectAllLeft?.addEventListener("click", function () {
            toggleAllOptions(available_options, selectAllLeft.checked);
            console.log('SABtn');
        });

        selectAllRight?.addEventListener("click", function () {
            toggleAllOptions(selected_options, selectAllRight.checked);
            console.log('RABtn');
        });

        function moveSelectedOptions(from, to) {
            console.log('moveSelected');
            [...from.selectedOptions].forEach(option => {
                option.selected = to === selected; // Ajusta a seleção ao mover
                to.appendChild(option);
            });

        }

        function toggleAllOptions(selectElement, checked) {
            console.log('toggleAll');
            for (let option of selectElement.options) {
                option.selected = checked;
            }
        }
    });
});
