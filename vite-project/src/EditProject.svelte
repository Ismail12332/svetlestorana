<script>
    import { onMount } from "svelte";
    import { useParams } from "svelte-navigator";
    import { writable } from "svelte/store";
    import { Link } from "svelte-navigator";

    let project = writable(null);

    const { subscribe } = useParams();


    //Гет запрос на сервер при переходе на страницу
    // Fetch project details when the component is mounted
    onMount(() => {
        const unsubscribe = subscribe((params) => {
        const { project_id } = params;

        fetchProjectDetails(project_id);
        });

        return unsubscribe;
    });

    async function fetchProjectDetails(project_id) {
        try {
        const response = await fetch(`http://127.0.0.1:5000/EditProject/${project_id}`, {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === "success") {
            // Convert ObjectId to string in the project data
            data.project._id = String(data.project._id);
            project.set(data.project);
            } else {
            console.error("Failed to fetch project details.");
            }
        } else {
            console.error("Failed to fetch project details.");
        }
        } catch (error) {
        console.error("Error during fetch:", error);
        }
    }

    // Добавьте вывод в консоль для отслеживания переменных
    $: {
        console.log('Current Section:', currentSection);
        console.log('Current Subsection:', currentSubsection);
        console.log('Opened Subsection:', openedSubsection);
    }
    
    // Обновленная функция addStep, которая добавляет шаг и обновляет соответствующий подраздел
    async function addStep(event) {
        event.preventDefault();

        const stepDescription = document.getElementById("step_description").value;
        const currentSection = document.getElementById("current_section").value;
        const currentSubsection = document.getElementById("current_subsection").value;

        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_step`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    section: currentSection,
                    subsection: currentSubsection,
                    step_description: stepDescription
                }),
            });

            const data = await response.json();
            console.log(data); // Можете обработать ответ от сервера здесь
            project.set(data.updated_project);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function addSteps(event, sectionName, subsectionName) {
        event.preventDefault();

        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_subsection_step`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `section_name=${encodeURIComponent(sectionName)}&subsection_name=${encodeURIComponent(subsectionName)}&step_description=${encodeURIComponent(stepDescription)}`,
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    project.set(data.updated_project);
                    closeCreateSubsectionModal();
                } else {
                    console.error("Failed to add step:", data.message);
                }
            } else {
                console.error("Failed to add step:", response.statusText);
            }
        } catch (error) {
            console.error("Error during add step:", error);
        }
    }

    $: {
        console.log("Project data:", $project);
    }
    ///Добавление раздела
    async function addSection(event) {
        event.preventDefault();

        const sectionName = document.getElementById("section_name").value;

        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_section`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `section_name=${encodeURIComponent(sectionName)}`,
            });

            if (response.ok) {
                const data = await response.json();  // Parse JSON response
                console.log("Section added successfully:", data);
                // Optionally, you can update the project data or refresh the page
                // based on your application's requirements.
                // For example, you can call a function to refresh project data.
                // refreshProjectData();
                project.set(data.updated_project);
                closeCreateSectionModal();
            } else {
                console.error("Failed to add section:", response.statusText);
            }
        } catch (error) {
            console.error("Error during add section:", error);
        }
    }


    let subsectionName = '';

    async function addSubsection(sectionName) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_subsection`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `section_name=${encodeURIComponent(sectionName)}&subsection_name=${encodeURIComponent(subsectionName)}`,
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    project.set(data.updated_project);
                    // Optionally, you can update the project data or refresh the page
                    // based on your application's requirements.
                    // For example, you can call a function to refresh project data.
                    // refreshProjectData();
                    closeCreateSubsectionModal();
                } else {
                    console.error("Failed to add subsection:", data.message);
                }
            } else {
                console.error("Failed to add subsection:", response.statusText);
            }
        } catch (error) {
            console.error("Error during add subsection:", error);
        }
    }
    /////////////////////////////////////////       Open close section     /////////////////////////////////////////

    ///Модальное окно для создания подразделов
    let currentSection = ""; // Add this variable

    function showCreateSubsectionModalStandard(sectionName) {
        console.log("Showing modal for section:", sectionName);
        currentSection = sectionName;
        var modal = document.getElementById("createSubsectionModalStandard");
        modal.style.display = "block";
    }

    function closeCreateSubsectionModalStandard () {
        var modal = document.getElementById("createSubsectionModalStandard");
        modal.style.display = "none";
        currentSection = "";
    }


    async function addStepStandard(event) {
        event.preventDefault();
        const currentSection = document.getElementById("current_section").value;
        const currentSubsection = document.getElementById("current_subsection").value;
        console.log(`section_name=${encodeURIComponent(currentSection)}&subsection_name=${encodeURIComponent(currentSubsection)}&step_description=${encodeURIComponent(stepDescription)}`);
        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_step_standard`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `section_name=${encodeURIComponent(currentSection)}&subsection_name=${encodeURIComponent(currentSubsection)}&step_description=${encodeURIComponent(stepDescription)}`,
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    console.log(data,'Step added successfully');
                    project.set(data.updated_project);
                    // Опционально: обновите данные проекта в Svelte store
                    // project.set(data.project);
                    stepDescription = "";
                    console.log(data.section)
                    // Опционально: очистите описание шага для будущих использований
                } else {
                    console.error("Failed to add step:", data.message);
                }
            } else {
                console.error("Failed to add step:", response.statusText);
            }
        } catch (error) {
            console.error("Error during add step:", error);
        }
    }

    async function addSubsectionStandard(sectionName) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_subsection_standard`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `section_name=${encodeURIComponent(sectionName)}&subsection_name=${encodeURIComponent(subsectionName)}`,
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    console.log('hello lox')
                    project.set(data.project);
                    // Optionally, you can update the project data or refresh the page
                    // based on your application's requirements.
                    // For example, you can call a function to refresh project data.
                    // refreshProjectData();
                    closeCreateSubsectionModalStandard();
                } else {
                    console.error("Failed to add subsection:", data.message);
                }
            } else {
                console.error("Failed to add subsection:", response.statusText);
            }
        } catch (error) {
            console.error("Error during add subsection:", error);
        }
    }

    function showCreateSubsectionModal(sectionName) {
        console.log("Showing modal for section:", sectionName);
        currentSection = sectionName; // Set the current section
        var modal = document.getElementById("createSubsectionModal");
        modal.style.display = "block";
    }

    function closeCreateSubsectionModal() {
        var modal = document.getElementById("createSubsectionModal");
        modal.style.display = "none";
        currentSection = ""; // Reset the current section when closing the modal
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
    
    let currentOpenSection = "";


    function showSubsections(sectionName) {
        closeAllSections();
        hideAddStepForm();
        closeSubsectionStandart();

        document.querySelectorAll('.infomation').forEach((section) => {
            section.style.display = 'none';
        });
        var subsectionsDiv = document.getElementById("subsections-" + sectionName);
        var sectionButton = document.getElementById(sectionName + "-button");

        if (currentOpenSection === sectionName) {
            // Если раздел уже открыт, то закрываем его
            subsectionsDiv.style.display = "none";
            currentOpenSection = "";
        } else {
            // Открываем выбранный раздел
            subsectionsDiv.style.display = "block";
            currentOpenSection = sectionName;
        }

        // Сбросьте цвет предыдущей кнопки и установите цвет для текущей кнопки
        resetButtonColor();
        sectionButton.classList.toggle("button-clicked");
    }


    //Модальное окно добавления раздела
    function showCreateSectionModal() {
        var modal = document.getElementById("createSectionModal");
        modal.style.display = "block";
    }

    function closeCreateSectionModal() {
        var modal = document.getElementById("createSectionModal");
        modal.style.display = "none";
    }



    let openedSubsectionse = null;

    function showSubsection(section, subsection) {
    hideAddStepForm();
    closeSubsectionStandart();
    stepRecommendations = '';
    // Проверяем, открыт ли уже этот подраздел
    if (openedSubsectionse === subsection) {
        // Если подраздел уже открыт, закрываем его
        openedSubsectionse = null;
    } else {
        // Если подраздел не открыт, открываем его
        openedSubsectionse = subsection;

        // Покажите форму "Add Step" и установите текущий раздел
        var addStepFormContainer = document.getElementById("add-step-form-container");
        addStepFormContainer.style.display = "block";
        currentSection = section;
        currentSubsection = subsection;
        var currentSectionField = document.getElementById("current_section");
        currentSectionField.value = section;
        var currentSubSectionField = document.getElementById("current_subsection");
        currentSubSectionField.value = subsection;
    }
}

    function resetButtonColor(sectionName) {
    // Найти все кнопки с классом "button-clicked" и удалить этот класс
    var clickedButtons = document.querySelectorAll('.button-clicked');
    clickedButtons.forEach(function (button) {
        if (button.id !== sectionName + "-button") {
            button.classList.remove('button-clicked');
        }
    });
}


function closeOtherSections(exceptSectionId) {
    // Закрытие разделов
    var sections = document.querySelectorAll(".osnova");
    sections.forEach(function (section) {
        if (section.id !== exceptSectionId) {
            section.style.display = "none";
        }
    });

    // Закрытие подразделов
    var subsections = document.querySelectorAll(".infomation");
    subsections.forEach(function (subsection) {
        if (subsection.id !== exceptSectionId) {
            subsection.style.display = "none";
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


function showIntroductionSections() {
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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
    closeSubsectionStandart();
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

    let addStepFormVisible = null;
    let stepDescription = "";

    function showAddStepForm(subsectionName) {
        addStepFormVisible = subsectionName;
    }

    function subsectionsDivStyle(sectionName) {
        return currentOpenSection && currentOpenSection === sectionName ? "block" : "none";
    }
    
    let currentSubsection = '';



    function closeSubsectionStandart () {
        var addStepFormContainer = document.getElementById("add-step-form-container_standard");
        addStepFormContainer.style.display = "none";
    }

    
    let openedSubsection = null;
    
    async function addImage(event) {
        event.preventDefault();

        const currentSection = document.getElementById("current_section").value;
        const currentSubsection = document.getElementById("current_subsection").value;
        const fileInput = document.getElementById('image_upload_input');
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/upload_image/${$project._id}/${currentSection}/${currentSubsection}`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                project.set(data.updated_project);
                // Обработка успешного ответа
            } else {
                console.error('Failed to upload image:', response.statusText);
            }
        } catch (error) {
            console.error('Error during image upload:', error);
        }
    }

    async function addStepsImage(event, sectionName, subsectionName) {
        event.preventDefault();
        
        try {
            const fileInput = document.getElementById('image_upload_input');
            const formData = new FormData();
            formData.append('file', fileInput.files[0]); // Первый файл из выбранных изображений

            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/${sectionName}/${subsectionName}/add_image`, {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    project.set(data.updated_project);
                    // Обновление данных в компоненте после успешной загрузки изображения
                    // Добавьте логику для сохранения URL изображения в соответствующем разделе и подразделе
                } else {
                    console.error("Failed to upload image:", data.message);
                }
            } else {
                console.error("Failed to upload image:", response.statusText);
            }
        } catch (error) {
            console.error("Error during image upload:", error);
        }
    }

    async function deleteImage(imageUrl, sectionName, subsectionName) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/${sectionName}/${subsectionName}/delete_image`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "image_url": imageUrl })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    project.set(data.updated_project);
                    // Обработка успешного удаления изображения
                } else {
                    console.error("Failed to delete image:", data.message);
                }
            } else {
                console.error("Failed to delete image:", response.statusText);
            }
        } catch (error) {
            console.error("Error during image deletion:", error);
        }
    }
    
    async function deleteImages(imageUrl, sectionName, subsectionName) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/${sectionName}/${subsectionName}/delete_images`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "image_url": imageUrl })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === "success") {
                project.set(data.updated_project);
                // Обновление пользовательского интерфейса после удаления фотографии
                // Например, обновление списка фотографий или перерисовка компонента
            } else {
                console.error("Failed to delete image:", data.message);
            }
        } else {
            console.error("Failed to delete image:", response.statusText);
        }
    } catch (error) {
        console.error("Error during image deletion:", error);
    }
}

    async function addImageStandard(event) {
        event.preventDefault();

        const formData = new FormData();
        const currentSection = document.getElementById("current_section").value;
        const currentSubSection = document.getElementById("current_subsection").value;
        const imageFile = document.getElementById("image_upload").files[0]; // Получаем файл из input
        console.log(currentSection)
        formData.append('section', currentSection);
        formData.append('subsection', currentSubSection);
        formData.append('image_upload', imageFile); // Добавляем файл в FormData

        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_imagestandard`, {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    project.set(data.updated_project);
                    // Обработка успешного ответа
                } else {
                    console.error("Failed to upload image:", data.message);
                }
            } else {
                console.error("Failed to upload image:", response.statusText);
            }
        } catch (error) {
            console.error("Error during image upload:", error);
        }
    }

    async function removeStep(step) {
        // Выполните запрос на сервер для удаления шага
        fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/remove_step`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                section: currentSection,
                subsection: currentSubsection,
                step_description: step
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Обработайте успешный ответ от сервера
            console.log(data);
            project.set(data.updated_project);
            // После успешного удаления обновите данные в вашем приложении
            // Это может включать в себя обновление $project или других необходимых переменных
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    async function removeImage(image) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/remove_image`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    image: image,
                    section: currentSection,
                    subsection: currentSubsection
                }),
            });

            const data = await response.json();
            console.log(data); // Можете обработать ответ от сервера здесь
            project.set(data.updated_project);

            // Если удаление успешно, обновите информацию на экране
            // Например, можно перезагрузить страницу или обновить список изображений без перезагрузки
        } catch (error) {
            console.error('Error:', error);
        }
    }

    let stepRecommendations = '';

    async function getStepRecommendations(section,subsection) {
        stepRecommendations = 'Наш бот уже отвечает на ваш запрос подождите...';
        const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/get-gpt-recommendations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ subsection,section, } )
        });

        if (response.ok) {
            const data = await response.json();
            stepRecommendations = data.recommendations; // Обновление переменной с рекомендациями
        } else {
            console.error('Ошибка при получении рекомендаций');
        }
    }
</script>

<style>

    main {
        width: 100%;
        height: 100%;
        color: rgb(255, 255, 255);
        background: linear-gradient(to bottom, #011a2b, #011529);
    }

    .top {
    display: flex;
    justify-content: space-evenly;
    margin: 15px;
    width: 92%;
}

button {
    margin: 13px;
    padding: 15px;
    border-radius: 10%;
    background-color: #d3be25f2;
}

.forplus {
    float: right;
    margin-right: 9%;
}

.forosnova {
    display: flex;
    justify-content: space-around;
}



.deck {
    margin-left: 2%;
}

.button-clicked {
    background-color: #14d424; /* Замените на желаемый цвет */
    color: rgb(141, 22, 22); /* Замените на желаемый цвет текста */
}

.subsection-button-clicked {
    background-color: #4CAF50; /* Замените на желаемый цвет */
    color: rgb(8, 5, 5); /* Замените на желаемый цвет текста */
}

.modal {
    display: none;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.7);
}

.modal-content {
    background-color: #fff;
    margin: 10% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 50%;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

h3 {
    color: #000000;
}

.formablack {
    color: #000000;
}

img {
    max-width: 200px; /* Максимальная ширина изображения будет равна ширине контейнера */
    max-height: 150px;/* Автоматическое вычисление высоты, чтобы сохранить пропорции */
}

.footer{
    height: 570px;
}

.steps {
    height: 300px;
    width: 1000px;
}
</style>



<main>
    {#if $project}
    <h1 class="sitename">Survzilla</h1>
    <Link to="/glav" class="btn btn-danger">Выйти из проекта</Link><!-- кнопка перехода на страницу создания проектов -->
    <div class="top">
        <h1>Edit Project: { $project.first_name } { $project.last_name } vessel name: { $project.vessel_name }</h1>
    </div>
    {/if}
    <div class="deck">
        <button id="introduction-sections-button" on:click={showIntroductionSections}>INTRODUCTION</button>
        <button id="hull-sections-button" on:click={showHullSections}>Hull, DECK & SUPERSTRUCTURE</button>
        <button id="above-sections-button" on:click={showAboveSections}>ABOVE</button>
        <button id="below-sections-button" on:click={showBelowSections}>BELOW</button>
        <button id="cathodic-protection-sections-button"  on:click={showCathodicProtectionSections}>CATHODIC PROTECTION</button>
        <button id="helm-station-sections-button" on:click={showHelmStationSections}>HELM STATION & NAVIGATIONAL</button>
        <button id="cabin-interior-sections-button" on:click={showCabinInteriorSections}>CABIN INTERIOR APPOINTMENTS</button>
        <button id="electrical-systems-button" on:click={showElectricalSystemsSections}>ELECTRICAL SYSTEMS</button>
        <button id="inboard-propulsion-sections-button" on:click={showInboardPropulsionSections}>INBOARD PROPULSION SYSTEM</button>
        <button id="steering-system-sections-button" on:click={showSteeringSystemSections}>STEERING SYSTEM</button>
        <button id="tankage-sections-button" on:click={showTankageSections}>TANKAGE</button>
        <button id="safety-equipment-sections-button" on:click={showSafetyEquipmentSections}>SAFETY EQUIPMENT</button>
        {#if $project && $project.sectionse && $project.sectionse.length > 0}
            {#each $project.sectionse as section (section)}
                <!-- Button to toggle subsections -->
                <button id="{ section.name }-button" on:click={() => showSubsections(section.name)}>{ section.name }</button>
            {/each}
        {/if}
        <button id="create-section-button" class="forplus" on:click={showCreateSectionModal}>+</button>

        <!--добавление подраздела-->
        <div id="createSubsectionModal" class="modal">
            <div class="modal-content">
                <span class="close" on:click={() => closeCreateSubsectionModal()}>&times;</span>
                <h3 class="formablack" color="black">Create New Subsection</h3>
                <form on:submit|preventDefault={() => addSubsection(currentSection)}>
                    <input type="hidden" bind:value={currentSection} />
                    <label class="formablack" for="subsection_name">Имя подраздела:</label>
                    <input type="text" bind:value={subsectionName} required>
                    <button class="formablack" type="submit">Добавить подраздел</button>
                </form>
            </div>
        </div>

        <!--добавление подраздела стандартные-->
        <div id="createSubsectionModalStandard" class="modal">
            <div class="modal-content">
                <span class="close" on:click={() => closeCreateSubsectionModalStandard()}>&times;</span>
                <h3 class="formablack" color="black">Create New Subsection</h3>
                <form on:submit|preventDefault={() => addSubsectionStandard(currentSection)}>
                    <input type="hidden" bind:value={currentSection} />
                    <label class="formablack" for="subsection_name">Имя подраздела:</label>
                    <input type="text" bind:value={subsectionName} required>
                    <button class="formablack" type="submit">Добавить подраздел</button>
                </form>
            </div>
        </div>
        
        {#if $project && $project.sectionse && $project.sectionse.length > 0}
            {#each $project.sectionse as section (section)}
                <!-- Button to toggle subsections -->
                <div id="subsections-{ section.name }" style="display: {subsectionsDivStyle(section.name)};" class="osnova">
                    <h1>{ section.name }</h1>
                    <button class="forplus" on:click={() => showCreateSubsectionModal(section.name)}>+</button>
                    <div id="{section.name}-subsections" class="subsections">
                        {#if section.subsections && section.subsections.length > 0}
                            {#each section.subsections as subsection (subsection)}
                                <div class="subsection">
                                    <button on:click={() => showAddStepForm(subsection.name)}>{subsection.name}</button>
                                    {#if addStepFormVisible === subsection.name}
                                        {#if subsection.cells && subsection.cells.length > 0}
                                        <div class="description-list">
                                        {#each subsection.cells as cell}
                                            {#if typeof cell === 'object'}
                                            <p>{cell.description}</p>
                                            {/if}
                                        {/each}
                                        </div>
                                    {/if}
                                    {#if subsection.images && subsection.images.length > 0}
                                        <div class="image-list">
                                            {#each subsection.images as image}
                                                <img src={image.image_url} alt="Image">
                                                <button on:click={() => deleteImage(image.image_url,section.name, subsection.name)}>Delete</button>
                                            {/each}
                                        </div>
                                    {/if}
                                        <form on:submit|preventDefault={(event) => addSteps(event, section.name, subsection.name)}>
                                            <label for="step_description">Step Description:</label>
                                            <input type="text" id="step_description" bind:value={stepDescription}>
                                            <button type="submit">Add Step</button>
                                        </form>
                                        <form on:submit|preventDefault={(event) => addStepsImage(event, section.name, subsection.name)}>
                                            <label for="image">Select Image:</label>
                                            <input type="file" id="image_upload_input" name="image">
                                            <button type="submit">Upload Image</button>
                                        </form>
                                    {/if}
                                </div>
                            {/each}
                        {/if}
                    </div>
                </div>
            {/each}
        {/if}
    </div>
    
    <div class="osnova" style="display: none;" id="introduction-sections">
        {#if $project && $project.sections && $project.sections.introduction}
            <h1>Introduction</h1>
            {#each Object.keys($project.sections.introduction) as key}
                <button id="{key}-button" on:click={() => showSubsection('introduction',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('introduction')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="hull-sections">
        {#if $project && $project.sections && $project.sections.hull}
            <h1>Hull</h1>
            {#each Object.keys($project.sections.hull) as key}
                <button id="{key}-button" on:click={() => showSubsection('hull',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('hull')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="above-sections">
        {#if $project && $project.sections && $project.sections.above}
            <h1>Above</h1>
            {#each Object.keys($project.sections.above) as key}
                <button id="{key}-button" on:click={() => showSubsection('above',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('above')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="below-sections">
        {#if $project && $project.sections && $project.sections.below}
            <h1>Below</h1>
            {#each Object.keys($project.sections.below) as key}
                <button id="{key}-button" on:click={() => showSubsection('below',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('below')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="cathodic-protection-sections">
        {#if $project && $project.sections && $project.sections.cathodic}
            <h1>Cathodic</h1>
            {#each Object.keys($project.sections.cathodic) as key}
                <button id="{key}-button" on:click={() => showSubsection('cathodic',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('cathodic')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="helm-station-sections">
        {#if $project && $project.sections && $project.sections.helm}
            <h1>Helm</h1>
            {#each Object.keys($project.sections.helm) as key}
                <button id="{key}-button" on:click={() => showSubsection('helm',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('helm')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="cabin-interior-sections">
        {#if $project && $project.sections && $project.sections.cabin}
            <h1>Cabin</h1>
            {#each Object.keys($project.sections.cabin) as key}
                <button id="{key}-button" on:click={() => showSubsection('cabin',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('cabin')}>+</button>
    </div>
    
    <div class="osnova" style="display: none;" id="electrical-systems-sections">
        {#if $project && $project.sections && $project.sections.electrical}
            <h1>Electrical</h1>
            {#each Object.keys($project.sections.electrical) as key}
                <button id="{key}-button" on:click={() => showSubsection('electrical',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('electrical')}>+</button>
    </div>
    
    <div class="osnova" style="display: none;" id="inboard-propulsion-sections">
        {#if $project && $project.sections && $project.sections.inboard}
            <h1>Inboard</h1>
            {#each Object.keys($project.sections.inboard) as key}
                <button id="{key}-button" on:click={() => showSubsection('inboard',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('inboard')}>+</button>
    </div>
    
    <div class="osnova" style="display: none;" id="steering-system-sections">
        {#if $project && $project.sections && $project.sections.steering}
            <h1>Steering</h1>
            {#each Object.keys($project.sections.steering) as key}
                <button id="{key}-button" on:click={() => showSubsection('steering',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('steering')}>+</button>
    </div>
    
    <div class="osnova" style="display: none;" id="tankage-sections">
        {#if $project && $project.sections && $project.sections.tankage}
            <h1>Tankage</h1>
            {#each Object.keys($project.sections.tankage) as key}
                <button id="{key}-button" on:click={() => showSubsection('tankage',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('tankage')}>+</button>
    </div>
    
    <div class="osnova" style="display: none;" id="safety-equipment-sections">
        {#if $project && $project.sections && $project.sections.safety}
            <h1>Safety</h1>
            {#each Object.keys($project.sections.safety) as key}
                <button id="{key}-button" on:click={() => showSubsection('safety',key)}>{key.replace(/_/g, ' ')}</button>
            {/each}
        {:else}
            <h1>no project</h1>
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('safety')}>+</button>
    </div>

    <!--Модальное окно добавления раздела-->
    <div id="createSectionModal" class="modal">
        <div class="modal-content">
            <span class="close" on:click={closeCreateSectionModal}>&times;</span>
            <h3 class="formablack" color="black">Create New Section</h3>
            <form on:submit={addSection}>
                <label class="formablack" for="section_name">Имя раздела:</label>
                <input type="text" name="section_name" id="section_name" required>
                <button type="submit">Name section</button>
            </form>
        </div>
    </div>

    
    <!--Добавление шага-->
    <div id="add-step-form-container" style="display: none;">
        <h2>Add Step:</h2>
        <h1>{currentSubsection.replace(/_/g, ' ')}</h1>
        <div id="step-recommendations">
            <p>{stepRecommendations}</p>
        </div>
        {#if $project && $project.sections && $project.sections[currentSection] && $project.sections[currentSection][currentSubsection] && $project.sections[currentSection][currentSubsection].images.length > 0}
            {#each $project.sections[currentSection][currentSubsection].images as image}
                <img src={image}/>
                <button on:click={() => removeImage(image)}>Remove</button>
            {/each}
        {/if}
        {#if $project && $project.sections && $project.sections[currentSection] && $project.sections[currentSection][currentSubsection] && $project.sections[currentSection][currentSubsection].steps.length}
            {#each $project.sections[currentSection][currentSubsection].steps as step}
            <div class="steps">    
                <li>{step}</li>
            </div>
                <button on:click={() => removeStep(step)}>Remove</button>
            {/each}
        {/if}
        <form on:submit={addStep}><!--<form method="POST" action="/edit_project/{{ project_id }}/add_step">-->
            <label for="step_description">Step Description:</label>
            <input type="text" id="step_description" name="step_description">
            <input type="hidden" name="subsection" id="current_subsection" value="">

            <input type="hidden" name="section" id="current_section" value="">
            <button type="submit">Add Step</button>
        </form>
        <form on:submit={addImageStandard}>
            <label for="image_upload">Select Image:</label>
            <input type="file" id="image_upload" name="image_upload">
            <input type="hidden" name="subsection" id="current_subsection" value="">
            <input type="hidden" name="section" id="current_section" value="">
            <button type="submit">Add Image</button>
        </form>
        <h2>Вы можете попросить момощи в осмотре яхты у нашего бота-помощника</h2>
        <button on:click={() => getStepRecommendations(currentSection,currentSubsection)}>Спросить помощника</button>
    </div>
    
    <!--Добавление шага стандартные разделы-->
    <div id="add-step-form-container_standard" style="display: none;">
        <h2>{openedSubsection}</h2>
        {#if $project && $project[currentSection] && $project[currentSection].length > 0}
            {#each $project[currentSection] as subsection}
                <div>
                    {#if openedSubsection === subsection.name}
                        {#if subsection.subsections && subsection.subsections.length > 0}
                            <div>
                                {#each subsection.subsections as step}
                                    <!-- Проверка, что это изображение -->
                                    {#if step.image_url}
                                        <img src={step.image_url} alt="Image">
                                        <button on:click={() => deleteImages(step.image_url, currentSection, subsection.name)}>Delete Photo</button>
                                    {/if}
                                    <!-- Если это не изображение, выведите описание шага -->
                                    {#if step.step_description}
                                        <p>{step.step_description}</p>
                                    {/if}
                                {/each}
                            </div>
                        {/if}
                    {/if}
                </div>
            {/each}
        {/if}
        <form on:submit={addStepStandard}>
            <label for="step_description">Step Description:</label>
            <input type="text" id="step_description" name="step_description" bind:value={stepDescription}>
            
            <input type="hidden" name="section" id="current_section" bind:value={currentSection}>
            <input type="hidden" name="subsection" id="current_subsection" bind:value={currentSubsection}>
            <button type="submit">Add Step</button>
        </form>
        <form on:submit={addImage}>
            <label for="image_upload_input">Upload Image:</label>
            <input type="hidden" name="section" id="current_section" bind:value={currentSection}>
            <input type="hidden" name="subsection" id="current_subsection" bind:value={currentSubsection}>
            <input type="file" id="image_upload_input" name="image_upload_input">
            <button type="submit">Upload Image</button>
        </form>
    </div>
    <div class='footer'>

    </div>
</main>