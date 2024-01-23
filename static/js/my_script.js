$(document).ready(function () {
    // Обработчик для формы добавления подраздела
    $("#add-subsection-form").submit(function (event) {
        event.preventDefault();
        var subsectionName = $("#subsection_name").val();
        if (subsectionName) {
            // Отправить форму, только если имя подраздела не пустое
            $(this).unbind("submit").submit();
        } else {
            alert("Введите имя подраздела.");
        }
    });

    // Обработчик для формы добавления ячейки
    $("#add-cell-form").submit(function (event) {
        event.preventDefault();
        var cellName = $("#cell_name").val();
        var cellDescription = $("#cell_description").val();
        if (cellName && cellDescription) {
            // Отправить форму, только если имя ячейки и описание не пустые
            $(this).unbind("submit").submit();
        } else {
            alert("Введите имя ячейки и описание.");
        }
    });
});




var currentOpenSubsection = null;
var currentOpenSubsectionButton = null;

function showSubsection(subsection) {
    var subsectionElement = document.getElementById(subsection + "-section");
    var subsectionButton = document.getElementById(subsection + "-button");

    // Если текущий подраздел открыт, смените его цвет обратно
    if (currentOpenSubsectionButton && currentOpenSubsectionButton !== subsectionButton) {
        currentOpenSubsectionButton.classList.remove("button-clicked");
    }

    // Переключите класс кнопки подраздела
    subsectionButton.classList.toggle("button-clicked");

    // Сохраните текущую кнопку подраздела
    currentOpenSubsectionButton = subsectionButton;

    if (currentOpenSubsection === subsection) {
        // If the same sub-section is clicked again, close it
        subsectionElement.style.display = "none";
        currentOpenSubsection = null;
    } else {
        // Close the previously open sub-section, if any
        if (currentOpenSubsection) {
            document.getElementById(currentOpenSubsection + "-section").style.display = "none";
        }

        // Close other subsections with the class "infomation"
        var allSubsections = document.querySelectorAll(".infomation");
        allSubsections.forEach(function (subsection) {
            if (subsection.id !== subsection + "-section") {
                subsection.style.display = "none";
            }
        });

        // Open the clicked sub-section
        subsectionElement.style.display = "block";
        currentOpenSubsection = subsection;
    }

    // Show the "Add Step" form and set the current section
    var addStepFormContainer = document.getElementById("add-step-form-container");
    addStepFormContainer.style.display = "block";
    var currentSectionField = document.getElementById("current_section");
    currentSectionField.value = subsection;
}

//Customer section show close
function showCreateSectionModal() {
    var modal = document.getElementById("createSectionModal");
    modal.style.display = "block";
}

function closeCreateSectionModal() {
    var modal = document.getElementById("createSectionModal");
    modal.style.display = "none";
}


function showSubsections(sectionName) {
    closeAllSections();
    var subsectionsDiv = document.getElementById("subsections-" + sectionName);

    // Сбросьте цвет предыдущей кнопки
    resetButtonColor(sectionName);
    

    if (subsectionsDiv.style.display === "none") {
        subsectionsDiv.style.display = "block";
    } else {
        subsectionsDiv.style.display = "none";
    }

    // Получите элемент кнопки
    var sectionButton = document.getElementById(sectionName + "-button");

    // Переключите класс кнопки
    sectionButton.classList.toggle("button-clicked");
}




function closeAllSections() {
    var allSections = document.querySelectorAll('.osnova');
    allSections.forEach(function (section) {
        section.style.display = "none";
    });

    // Сбросьте цвет всех кнопок
    var allButtons = document.querySelectorAll('.button-clicked');
    allButtons.forEach(function (button) {
        button.classList.remove('button-clicked');
    });
}



//Customer subsection show close
function showCreateSubsectionModal(sectionName) {
    var modal = document.getElementById("createSubsectionModal");
    var input = modal.querySelector("#section_name_input");

    input.value = sectionName;

    modal.style.display = "block";
}

function closeCreateSubsectionModal() {
    var modal = document.getElementById("createSubsectionModal");
    modal.style.display = "none";
}



//Customer cells show close
function showCreateCellModal(sectionName, subsectionName) {
    var modal = document.getElementById("createCellModal");
    var sectionInput = modal.querySelector("#section_name_input");
    var subsectionInput = modal.querySelector("#subsection_name_input");

    sectionInput.value = sectionName;
    subsectionInput.value = subsectionName;

    modal.style.display = "block";
}

function closeCreateCellModal() {
    var modal = document.getElementById("createCellModal");
    modal.style.display = "none";
}
//
function showCells(sectionName, subsectionName) {
    var cellsDiv = document.getElementById("cells-" + sectionName + "-" + subsectionName);

    if (cellsDiv.style.display === "none") {
        cellsDiv.style.display = "block";
    } else {
        cellsDiv.style.display = "none";
    }
}


function showCellInfo(sectionName, subsectionName, cellName) {
    var cellInfo = document.getElementById(`cellInfo-${sectionName}-${subsectionName}-${cellName}`);
    if (cellInfo.style.display === "none") {
        cellInfo.style.display = "block";
    } else {
        cellInfo.style.display = "none";
    }
}

function closeOtherSections(exceptSectionId) {
    var sections = document.querySelectorAll(".osnova");
    sections.forEach(function (section) {
        if (section.id !== exceptSectionId) {
            section.style.display = "none";
        }
    });
}





function hideOtherSections(exceptSectionId) {
    // Get all sections except the one specified by exceptSectionId
    var sections = document.querySelectorAll(".infomation");
    sections.forEach(function (section) {
        if (section.id !== exceptSectionId) {
            section.style.display = "none";
        }
    });
}

function hideAddStepForm() {
    var addStepFormContainer = document.getElementById("add-step-form-container");
    addStepFormContainer.style.display = "none";
}

function closeSubsections(sectionId) {
    var section = document.getElementById(sectionId);
    if (section) {
        var subsections = section.getElementsByClassName("infomation"); // Replace "infomation" with the class name of your subsections
        for (var i = 0; i < subsections.length; i++) {
            subsections[i].style.display = "none";
        }
    }
}


//----------------------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------------------
function resetButtonColor(sectionName) {
    // Найти все кнопки с классом "button-clicked" и удалить этот класс
    var clickedButtons = document.querySelectorAll('.button-clicked');
    clickedButtons.forEach(function (button) {
        if (button.id !== sectionName + "-button") {
            button.classList.remove('button-clicked');
        }
    });
}

function resetSubsectionButtonColor() {
    // Найти все кнопки с классом "button-clicked" и удалить этот класс
    var clickedButtons = document.querySelectorAll('.subsection-button-clicked');
    clickedButtons.forEach(function (button) {
        button.classList.remove('subsection-button-clicked');
    });
}


function showIntroductionSections() {
    // Закройте другие разделы
    closeOtherSections("introduction-sections");
    closeSubsections("introduction-sections");
    hideAddStepForm();

    // Сбросьте цвет предыдущей кнопки
    resetButtonColor();

    // Получите элемент кнопки
    var introductionSectionsButton = document.getElementById("introduction-sections-button");

    // Переключите класс кнопки
    introductionSectionsButton.classList.toggle("button-clicked");

    // Получите элемент секции
    var introductionSections = document.getElementById("introduction-sections");

    // Переключите отображение секции
    if (introductionSections.style.display === "none") {
        introductionSections.style.display = "block";
    } else {
        introductionSections.style.display = "none";
    }
}

function showElectricalSystemsSections() {
    closeOtherSections("electrical-systems-sections");
    closeSubsections("electrical-systems-sections");
    hideAddStepForm();

    // Сбросьте цвет предыдущей кнопки
    resetButtonColor();

    // Получите элемент кнопки
    var electricalSystemsButton = document.getElementById("electrical-systems-button");

    // Переключите класс кнопки
    electricalSystemsButton.classList.toggle("button-clicked");

    // Получите элемент секции
    var electricalSystemsSections = document.getElementById("electrical-systems-sections");

    // Переключите отображение секции
    if (electricalSystemsSections.style.display === "none") {
        electricalSystemsSections.style.display = "block";
    } else {
        electricalSystemsSections.style.display = "none";
    }
}



//HullSections
function showHullSections() {
    // Закройте другие разделы
    closeOtherSections("hull-sections");
    closeSubsections("hull-sections");
    hideAddStepForm();

    // Сбросьте цвет предыдущей кнопки
    resetButtonColor();

    // Получите элемент кнопки
    var hullSectionsButton = document.getElementById("hull-sections-button");

    // Переключите класс кнопки
    hullSectionsButton.classList.toggle("button-clicked");

    // Получите элемент секции
    var hullSections = document.getElementById("hull-sections");

    // Переключите отображение секции
    if (hullSections.style.display === "none") {
        hullSections.style.display = "block";
    } else {
        hullSections.style.display = "none";
    }
}


function showAboveSections() {
    // Закройте другие разделы
    closeOtherSections("above-sections");
    closeSubsections("above-sections");
    hideAddStepForm();

    // Сбросьте цвет предыдущей кнопки
    resetButtonColor();

    // Получите элемент кнопки
    var aboveSectionsButton = document.getElementById("above-sections-button");

    // Переключите класс кнопки
    aboveSectionsButton.classList.toggle("button-clicked");

    // Получите элемент секции
    var aboveSections = document.getElementById("above-sections");

    // Переключите отображение секции
    if (aboveSections.style.display === "none") {
        aboveSections.style.display = "block";
    } else {
        aboveSections.style.display = "none";
    }
}

// Повторите тот же шаблон для других функций
function showBelowSections() {
    closeOtherSections("below-sections");
    closeSubsections("below-sections");
    hideAddStepForm();

    resetButtonColor();

    var belowSectionsButton = document.getElementById("below-sections-button");

    belowSectionsButton.classList.toggle("button-clicked");

    var belowSections = document.getElementById("below-sections");

    if (belowSections.style.display === "none") {
        belowSections.style.display = "block";
    } else {
        belowSections.style.display = "none";
    }
}

// Повторите тот же шаблон для других функций
function showCathodicProtectionSections() {
    closeOtherSections("cathodic-protection-sections");
    closeSubsections("cathodic-protection-sections");
    hideAddStepForm();

    resetButtonColor();

    var cathodicProtectionSectionsButton = document.getElementById("cathodic-protection-sections-button");

    cathodicProtectionSectionsButton.classList.toggle("button-clicked");

    var cathodicProtectionSections = document.getElementById("cathodic-protection-sections");

    if (cathodicProtectionSections.style.display === "none") {
        cathodicProtectionSections.style.display = "block";
    } else {
        cathodicProtectionSections.style.display = "none";
    }
}

//Helm Sections
function showHelmStationSections() {
    closeOtherSections("helm-station-sections");
    closeSubsections("helm-station-sections");
    hideAddStepForm();
    resetButtonColor();

    var helmStationSectionsButton = document.getElementById("helm-station-sections-button");

    helmStationSectionsButton.classList.toggle("button-clicked");

    var helmStationSections = document.getElementById("helm-station-sections");

    if (helmStationSections.style.display === "none") {
        helmStationSections.style.display = "block";
    } else {
        helmStationSections.style.display = "none";
    }
}

function showCabinInteriorSections() {
    closeOtherSections("cabin-interior-sections");
    closeSubsections("cabin-interior-sections");
    hideAddStepForm();
    resetButtonColor();

    var cabinInteriorSectionsButton = document.getElementById("cabin-interior-sections-button");

    cabinInteriorSectionsButton.classList.toggle("button-clicked");

    var cabinInteriorSections = document.getElementById("cabin-interior-sections");

    if (cabinInteriorSections.style.display === "none") {
        cabinInteriorSections.style.display = "block";
    } else {
        cabinInteriorSections.style.display = "none";
    }
}

function showInboardPropulsionSections() {
    closeOtherSections("inboard-propulsion-sections");
    closeSubsections("inboard-propulsion-sections");
    hideAddStepForm();
    resetButtonColor();

    var inboardPropulsionSectionsButton = document.getElementById("inboard-propulsion-sections-button");

    inboardPropulsionSectionsButton.classList.toggle("button-clicked");

    var inboardPropulsionSections = document.getElementById("inboard-propulsion-sections");

    if (inboardPropulsionSections.style.display === "none") {
        inboardPropulsionSections.style.display = "block";
    } else {
        inboardPropulsionSections.style.display = "none";
    }
}

function showSteeringSystemSections() {
    closeOtherSections("steering-system-sections");
    closeSubsections("steering-system-sections");
    hideAddStepForm();
    resetButtonColor();

    var steeringSystemSectionsButton = document.getElementById("steering-system-sections-button");

    steeringSystemSectionsButton.classList.toggle("button-clicked");

    var steeringSystemSections = document.getElementById("steering-system-sections");

    if (steeringSystemSections.style.display === "none") {
        steeringSystemSections.style.display = "block";
    } else {
        steeringSystemSections.style.display = "none";
    }
}


function showTankageSections() {
    closeOtherSections("tankage-sections");
    closeSubsections("tankage-sections");
    hideAddStepForm();
    resetButtonColor();

    var tankageSectionsButton = document.getElementById("tankage-sections-button");

    tankageSectionsButton.classList.toggle("button-clicked");

    var tankageSections = document.getElementById("tankage-sections");

    if (tankageSections.style.display === "none") {
        tankageSections.style.display = "block";
    } else {
        tankageSections.style.display = "none";
    }
}

function showSafetyEquipmentSections() {
    closeOtherSections("safety-equipment-sections");
    closeSubsections("safety-equipment-sections");
    hideAddStepForm();
    resetButtonColor();

    var safetyEquipmentSectionsButton = document.getElementById("safety-equipment-sections-button");

    safetyEquipmentSectionsButton.classList.toggle("button-clicked");

    var safetyEquipmentSections = document.getElementById("safety-equipment-sections");

    if (safetyEquipmentSections.style.display === "none") {
        safetyEquipmentSections.style.display = "block";
    } else {
        safetyEquipmentSections.style.display = "none";
    }
}

