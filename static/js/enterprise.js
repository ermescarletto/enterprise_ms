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
       const widgets = document.querySelectorAll(".dual-list-widget");
            widgets.forEach(widget => {
                const availableList = widget.querySelector(".available-list");
                const selectedList = widget.querySelector(".selected-list");
                const addBtn = widget.querySelector(".move-right");
                const removeBtn = widget.querySelector(".move-left");
                const selectAllLeft = widget.querySelector(".select-all-left");
                const selectAllRight = widget.querySelector(".select-all-right");

                addBtn.addEventListener("click", () => {
                    moveSelectedOptions(availableList, selectedList);
                });

                removeBtn.addEventListener("click", () => {
                    moveSelectedOptions(selectedList, availableList);
                });

                selectAllLeft.addEventListener("change", () => {
                    toggleAllOptions(availableList, selectAllLeft.checked);
                });

                selectAllRight.addEventListener("change", () => {
                    toggleAllOptions(selectedList, selectAllRight.checked);
                });

                function moveSelectedOptions(from, to) {
                    Array.from(from.selectedOptions).forEach(option => {
                        to.appendChild(option);
                    });
                }

                function toggleAllOptions(selectElement, checked) {
                    Array.from(selectElement.options).forEach(option => {
                        option.selected = checked;
                    });
                }
            });

