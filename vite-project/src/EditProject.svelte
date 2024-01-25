<script>
    import { onMount } from "svelte";
    import { useParams } from "svelte-navigator";
    import { writable } from "svelte/store";
    import { Link } from "svelte-navigator";

    let project = writable(null);

    const { subscribe } = useParams();

    let certification_steps = writable([]);
    let purpose_of_survey_steps = writable([]);
    let circumstances_of_survey_steps = writable([]);
    let report_file_no_steps = writable([]);
    let surveyor_qualifications_steps = writable([]);
    let intended_use_steps = writable([]);
    let gen_info_steps = writable([]);
    let layout_overview_steps = writable([]);
    let design_steps = writable([]);
    let deck_steps = writable([]);
    let structural_members_steps = writable([]);
    let bottom_paint_steps = writable([]);
    let blister_comment_steps = writable([]);
    let transom_steps = writable([]);
    let deck_floor_plan_steps = writable([]);
    let anchor_platform_steps = writable([]);
    let toe_rails_steps = writable([]);
    let mooring_hardware_steps = writable([]);
    let hatches_steps = writable([]);
    let exterior_seating_steps = writable([]);
    let cockpit_equipment_steps = writable([]);
    let ngine_hatch_steps = writable([]);
    let above_draw_water_line_steps = writable([]);
    let boarding_ladder_steps = writable([]);
    let swim_platform_steps = writable([]);
    let below_draw_water_steps = writable([]);
    let thru_hull_strainers_steps = writable([]);
    let transducer_steps = writable([]);
    let sea_valves_steps = writable([]);
    let sea_strainers_steps = writable([]);
    let trim_tabs_steps = writable([]);
    let note_steps = writable([]);
    let bonding_system_steps =writable([]);
    let anodes_steps = writable([]);
    let lightning_protection_steps = writable([]);
    let additional_remarks_steps = writable([]);
    let helm_station_steps = writable([]);
    let throttle_shift_controls_steps = writable([]);
    let engine_room_blowers_steps = writable([]);
    let engine_status_steps = writable([]);
    let other_electronics_controls_steps = writable([]);
    let entertainment_berthing_steps = writable([]);
    let interior_lighting_steps = writable([]);
    let galley_dinette_steps = writable([]);
    let water_closets_steps = writable([]);
    let climate_control_steps = writable([]);
    let dc_systems_type_steps = writable([]);
    let ac_systems_steps = writable([]);
    let generator_steps = writable([]);
    let engines_steps = writable([]);
    let serial_numbers_steps = writable([]);
    let engine_hours_steps = writable([]);
    let other_note_steps = writable([]);
    let reverse_gears_steps = writable([]);
    let shafting_propellers_steps = writable([]);
    let manufacture_steps = writable([]);
    let steering_components_steps = writable([]);
    let fuel_tank_steps = writable([]);
    let potable_water_system_steps = writable([]);
    let holding_tank_black_water_steps = writable([]);
    let life_jackets_steps = writable([]);
    let navigational_lights_steps = writable([]);
    let throwable_pfd_steps = writable([]);
    let visual_distress_signals_steps = writable([]);
    let sound_devices_steps = writable([]);
    let uscg_placards_steps =writable([]);
    let flame_arrestors_steps = writable([]);
    let engine_ventilation_steps = writable([]);
    let ignition_protection_steps = writable([]);
    let inland_navigational_rule_book_steps = writable([]);
    let waste_management_plan_steps = writable([]);
    let fire_fighting_equipment_steps = writable([]);
    let bilge_pumps_steps = writable([]);
    let ground_tackle_windlass_steps = writable([]);
    let auxiliary_safety_equipment_steps = writable([]);

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
        console.log("certification_steps:", certification_steps);
        console.log("purpose_of_survey_steps:", purpose_of_survey_steps);
        console.log("circumstances_of_survey_steps:", circumstances_of_survey_steps);
        console.log('Current Section:', currentSection);
        console.log('Opened Subsection:', openedSubsection);
    }


    //Добавления шага
    

    // ... (ваш существующий код)

    // Обновленная функция addStep, которая добавляет шаг и обновляет соответствующий подраздел
    async function addStep(event, sectionName) {
        event.preventDefault();

        const stepDescription = document.getElementById("step_description").value;
        const currentSection = document.getElementById("current_section").value;

        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_step`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `step_description=${encodeURIComponent(stepDescription)}&section=${encodeURIComponent(currentSection)}`,
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    // Обновляем certification_steps после успешного добавления шага
                    project.update((prev) => ({
                        ...prev,
                        certification_steps: data.updated_project.certification_steps,
                        purpose_of_survey_steps: data.updated_project.purpose_of_survey_steps,
                        circumstances_of_survey_steps: data.updated_project.circumstances_of_survey_steps,
                        report_file_no_steps: data.updated_project.report_file_no_steps,
                        surveyor_qualifications_steps: data.updated_project.surveyor_qualifications_steps,
                        intended_use_steps: data.updated_project.intended_use_steps,
                        gen_info_steps: data.updated_project.gen_info_steps,
                        layout_overview_steps: data.updated_project.layout_overview_steps,
                        design_steps: data.updated_project.design_steps,
                        deck_steps: data.updated_project.deck_steps,
                        structural_members_steps: data.updated_project.structural_members_steps,
                        bottom_paint_steps: data.updated_project.bottom_paint_steps,
                        blister_comment_steps: data.updated_project.blister_comment_steps,
                        transom_steps: data.updated_project.transom_steps,
                        deck_floor_plan_steps: data.updated_project.deck_floor_plan_steps,
                        anchor_platform_steps: data.updated_project.anchor_platform_steps,
                        toe_rails_steps: data.updated_project.toe_rails_steps,
                        mooring_hardware_steps: data.updated_project.mooring_hardware_steps,
                        hatches_steps: data.updated_project.hatches_steps,
                        exterior_seating_steps: data.updated_project.exterior_seating_steps,
                        cockpit_equipment_steps: data.updated_project.cockpit_equipment_steps,
                        ngine_hatch_steps: data.updated_project.ngine_hatch_steps,
                        above_draw_water_line_steps: data.updated_project.above_draw_water_line_steps,
                        boarding_ladder_steps: data.updated_project.boarding_ladder_steps,
                        swim_platform_steps: data.updated_project.swim_platform_steps,
                        below_draw_water_steps: data.updated_project.below_draw_water_steps,
                        thru_hull_strainers_steps: data.updated_project.thru_hull_strainers_steps,
                        transducer_steps: data.updated_project.transducer_steps,
                        sea_valves_steps: data.updated_project.sea_valves_steps,
                        sea_strainers_steps: data.updated_project.sea_strainers_steps,
                        trim_tabs_steps: data.updated_project.trim_tabs_steps,
                        note_steps: data.updated_project.note_steps,
                        bonding_system_steps: data.updated_project.bonding_system_steps,
                        anodes_steps: data.updated_project.anodes_steps,
                        lightning_protection_steps: data.updated_project.lightning_protection_steps,
                        additional_remarks_steps: data.updated_project.additional_remarks_steps,
                        helm_station_steps: data.updated_project.helm_station_steps,
                        throttle_shift_controls_steps: data.updated_project.throttle_shift_controls_steps,
                        engine_room_blowers_steps: data.updated_project.engine_room_blowers_steps,
                        engine_status_steps: data.updated_project.engine_status_steps,
                        other_electronics_controls_steps: data.updated_project.other_electronics_controls_steps,
                        entertainment_berthing_steps: data.updated_project.entertainment_berthing_steps,
                        interior_lighting_steps: data.updated_project.interior_lighting_steps,
                        galley_dinette_steps: data.updated_project.galley_dinette_steps,
                        water_closets_steps: data.updated_project.water_closets_steps,
                        climate_control_steps: data.updated_project.climate_control_steps,
                        dc_systems_type_steps: data.updated_project.dc_systems_type_steps,
                        ac_systems_steps: data.updated_project.ac_systems_steps,
                        generator_steps: data.updated_project.generator_steps,
                        engines_steps: data.updated_project.engines_steps,
                        serial_numbers_steps: data.updated_project.serial_numbers_steps,
                        engine_hours_steps: data.updated_project.engine_hours_steps,
                        other_note_steps: data.updated_project.other_note_steps,
                        reverse_gears_steps: data.updated_project.reverse_gears_steps,
                        shafting_propellers_steps: data.updated_project.shafting_propellers_steps,
                        manufacture_steps: data.updated_project.manufacture_steps,
                        steering_components_steps: data.updated_project.steering_components_steps,
                        fuel_tank_steps: data.updated_project.fuel_tank_steps,
                        potable_water_system_steps: data.updated_project.potable_water_system_steps,
                        holding_tank_black_water_steps: data.updated_project.holding_tank_black_water_steps,
                        life_jackets_steps: data.updated_project.life_jackets_steps,
                        navigational_lights_steps: data.updated_project.navigational_lights_steps,
                        throwable_pfd_steps: data.updated_project.throwable_pfd_steps,
                        visual_distress_signals_steps: data.updated_project.visual_distress_signals_steps,
                        sound_devices_steps: data.updated_project.sound_devices_steps,
                        uscg_placards_steps: data.updated_project.uscg_placards_steps,
                        flame_arrestors_steps: data.updated_project.flame_arrestors_steps,
                        engine_ventilation_steps: data.updated_project.engine_ventilation_steps,
                        ignition_protection_steps: data.updated_project.ignition_protection_steps,
                        inland_navigational_rule_book_steps: data.updated_project.inland_navigational_rule_book_steps,
                        waste_management_plan_steps: data.updated_project.waste_management_plan_steps,
                        fire_fighting_equipment_steps: data.updated_project.fire_fighting_equipment_steps,
                        bilge_pumps_steps: data. updated_project.bilge_pumps_steps,
                        ground_tackle_windlass_steps: data.updated_project.ground_tackle_windlass_steps,
                        auxiliary_safety_equipment_steps: data.updated_project.auxiliary_safety_equipment_steps,
                    }));
                    // Очищаем поле ввода после успешного добавления
                    document.getElementById("step_description").value = '';
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

    //Удаление шага
    async function deleteStep(section, step) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/delete_step`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `step_to_delete=${encodeURIComponent(step)}&section=${encodeURIComponent(section)}`,
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    // Обновите certification_steps после успешного удаления шага
                    project.update((prev) => ({
                        ...prev,
                        certification_steps: data.updated_project.certification_steps,
                        purpose_of_survey_steps: data.updated_project.purpose_of_survey_steps,
                        circumstances_of_survey_steps: data.updated_project.circumstances_of_survey_steps,
                        report_file_no_steps: data.updated_project.report_file_no_steps,
                        surveyor_qualifications_steps: data.updated_project.surveyor_qualifications_steps,
                        intended_use_steps: data.updated_project.intended_use_steps,
                        gen_info_steps: data.updated_project.gen_info_steps,
                        layout_overview_steps: data.updated_project.layout_overview_steps,
                        design_steps: data.updated_project.design_steps,
                        deck_steps: data.updated_project.deck_steps,
                        structural_members_steps: data.updated_project.structural_members_steps,
                        bottom_paint_steps: data.updated_project.bottom_paint_steps,
                        blister_comment_steps: data.updated_project.blister_comment_steps,
                        transom_steps: data.updated_project.transom_steps,
                        deck_floor_plan_steps: data.updated_project.deck_floor_plan_steps,
                        anchor_platform_steps: data.updated_project.anchor_platform_steps,
                        toe_rails_steps: data.updated_project.toe_rails_steps,
                        mooring_hardware_steps: data.updated_project.mooring_hardware_steps,
                        hatches_steps: data.updated_project.hatches_steps,
                        exterior_seating_steps: data.updated_project.exterior_seating_steps,
                        cockpit_equipment_steps: data.updated_project.cockpit_equipment_steps,
                        ngine_hatch_steps: data.updated_project.ngine_hatch_steps,
                        above_draw_water_line_steps: data.updated_project.above_draw_water_line_steps,
                        boarding_ladder_steps: data.updated_project.boarding_ladder_steps,
                        swim_platform_steps: data.updated_project.swim_platform_steps,
                        below_draw_water_steps: data.updated_project.below_draw_water_steps,
                        thru_hull_strainers_steps: data.updated_project.thru_hull_strainers_steps,
                        transducer_steps: data.updated_project.transducer_steps,
                        sea_valves_steps: data.updated_project.sea_valves_steps,
                        sea_strainers_steps: data.updated_project.sea_strainers_steps,
                        trim_tabs_steps: data.updated_project.trim_tabs_steps,
                        note_steps: data.updated_project.note_steps,
                        bonding_system_steps: data.updated_project.bonding_system_steps,
                        anodes_steps: data.updated_project.anodes_steps,
                        lightning_protection_steps: data.updated_project.lightning_protection_steps,
                        additional_remarks_steps: data.updated_project.additional_remarks_steps,
                        helm_station_steps: data.updated_project.helm_station_steps,
                        throttle_shift_controls_steps: data.updated_project.throttle_shift_controls_steps,
                        engine_room_blowers_steps: data.updated_project.engine_room_blowers_steps,
                        engine_status_steps: data.updated_project.engine_status_steps,
                        other_electronics_controls_steps: data.updated_project.other_electronics_controls_steps,
                        entertainment_berthing_steps: data.updated_project.entertainment_berthing_steps,
                        interior_lighting_steps: data.updated_project.interior_lighting_steps,
                        galley_dinette_steps: data.updated_project.galley_dinette_steps,
                        water_closets_steps: data.updated_project.water_closets_steps,
                        climate_control_steps: data.updated_project.climate_control_steps,
                        dc_systems_type_steps: data.updated_project.dc_systems_type_steps,
                        ac_systems_steps: data.updated_project.ac_systems_steps,
                        generator_steps: data.updated_project.generator_steps,
                        engines_steps: data.updated_project.engines_steps,
                        serial_numbers_steps: data.updated_project.serial_numbers_steps,
                        engine_hours_steps: data.updated_project.engine_hours_steps,
                        other_note_steps: data.updated_project.other_note_steps,
                        reverse_gears_steps: data.updated_project.reverse_gears_steps,
                        shafting_propellers_steps: data.updated_project.shafting_propellers_steps,
                        manufacture_steps: data.updated_project.manufacture_steps,
                        steering_components_steps: data.updated_project.steering_components_steps,
                        fuel_tank_steps: data.updated_project.fuel_tank_steps,
                        potable_water_system_steps: data.updated_project.potable_water_system_steps,
                        holding_tank_black_water_steps: data.updated_project.holding_tank_black_water_steps,
                        life_jackets_steps: data.updated_project.life_jackets_steps,
                        navigational_lights_steps: data.updated_project.navigational_lights_steps,
                        throwable_pfd_steps: data.updated_project.throwable_pfd_steps,
                        visual_distress_signals_steps: data.updated_project.visual_distress_signals_steps,
                        sound_devices_steps: data.updated_project.sound_devices_steps,
                        uscg_placards_steps: data.updated_project.uscg_placards_steps,
                        flame_arrestors_steps: data.updated_project.flame_arrestors_steps,
                        engine_ventilation_steps: data.updated_project.engine_ventilation_steps,
                        ignition_protection_steps: data.updated_project.ignition_protection_steps,
                        inland_navigational_rule_book_steps: data.updated_project.inland_navigational_rule_book_steps,
                        waste_management_plan_steps: data.updated_project.waste_management_plan_steps,
                        fire_fighting_equipment_steps: data.updated_project.fire_fighting_equipment_steps,
                        bilge_pumps_steps: data. updated_project.bilge_pumps_steps,
                        ground_tackle_windlass_steps: data.updated_project.ground_tackle_windlass_steps,
                        auxiliary_safety_equipment_steps: data.updated_project.auxiliary_safety_equipment_steps,
                    }));
                } else {
                    console.error("Failed to delete step:", data.message);
                }
            } else {
                console.error("Failed to delete step:", response.statusText);
            }
        } catch (error) {
            console.error("Error during delete step:", error);
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

    var currentOpenSubsection = null;
    var currentOpenSubsectionButton = null;

    function showSubsection(subsection) {
    hideAddStepForm();
    closeSubsectionStandart();
    var subsectionElement = document.getElementById(subsection + "-section");
    var subsectionButton = document.getElementById(subsection + "-button");

    // Если текущий подраздел открыт, скройте форму добавления шага
    if (currentOpenSubsection === subsection) {
        hideAddStepForm();
        currentOpenSubsection = null;

        // Смените цвет кнопки подраздела обратно
        if (currentOpenSubsectionButton) {
            currentOpenSubsectionButton.classList.remove("button-clicked");
        }

        // Очистите текущую кнопку подраздела
        currentOpenSubsectionButton = null;

        // Скройте текущий подраздел
        subsectionElement.style.display = "none";
    } else {
        // Закройте предыдущий открытый подраздел, если есть
        if (currentOpenSubsection) {
            document.getElementById(currentOpenSubsection + "-section").style.display = "none";
        }

        // Закройте другие подразделы с классом "infomation"
        var allSubsections = document.querySelectorAll(".infomation");
        allSubsections.forEach(function (subsection) {
            if (subsection.id !== subsection + "-section") {
                subsection.style.display = "none";
            }
        });

        // Откройте выбранный подраздел
        subsectionElement.style.display = "block";
        currentOpenSubsection = subsection;

        // Переключите класс кнопки подраздела
        subsectionButton.classList.add("button-clicked");

        // Сохраните текущую кнопку подраздела
        currentOpenSubsectionButton = subsectionButton;

        // Покажите форму "Add Step" и установите текущий раздел
        var addStepFormContainer = document.getElementById("add-step-form-container");
        addStepFormContainer.style.display = "block";
        var currentSectionField = document.getElementById("current_section");
        currentSectionField.value = subsection;
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

function resetSubsectionButtonColor() {
    // Найти все кнопки с классом "button-clicked" и удалить этот класс
    var clickedButtons = document.querySelectorAll('.subsection-button-clicked');
    clickedButtons.forEach(function (button) {
        button.classList.remove('subsection-button-clicked');
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

    function showSubsectionStandart(sectionName, subsectionName) {
        hideAddStepForm();

        document.querySelectorAll('.infomation').forEach((section) => {
            section.style.display = 'none';
        });

        // Logic to display the form
        var addStepFormContainer = document.getElementById("add-step-form-container_standard");
        addStepFormContainer.style.display = "block";

        // Set values for both section and subsection
        var currentSectionField = document.getElementById("current_section");
        currentSectionField.value = sectionName;

        var currentSubsectionField = document.getElementById("current_subsection");
        currentSubsectionField.value = subsectionName;

        openedSubsection = subsectionName;

        currentSection = sectionName;

        console.log(currentSectionField.value, currentSubsectionField.value);
        // Additional logic if needed
    }

    function closeSubsectionStandart () {
        var addStepFormContainer = document.getElementById("add-step-form-container_standard");
        addStepFormContainer.style.display = "none";
    }

    function closeEverethingOpenSection () {
        var OpenSection = document.getElementById(".information")
        OpenSection.style.display = "none";
    }
    
    let openedSubsection = null;
    
</script>

<style>

    main {
        width: 100%;
        height: 1200px;
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
    color: rgb(0, 0, 0); /* Замените на желаемый цвет текста */
}

.subsection-button-clicked {
    background-color: #4CAF50; /* Замените на желаемый цвет */
    color: white; /* Замените на желаемый цвет текста */
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
        
        {#if $project && $project.sections && $project.sections.length > 0}
            {#each $project.sections as section (section)}
                <!-- Button to toggle subsections -->
                <button id="{ section.name }-button" on:click={() => showSubsections(section.name)}>{ section.name }</button>
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
                                        <form on:submit|preventDefault={(event) => addSteps(event, section.name, subsection.name)}>
                                            <label for="step_description">Step Description:</label>
                                            <input type="text" id="step_description" bind:value={stepDescription}>
                                            <button type="submit">Add Step</button>
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
        <h1 class="forosnova">Introduction sections</h1>
        <button id="gen_info-button" on:click={() => showSubsection('gen_info')}>Genera Vessel Info</button>
        <button id="certification-button" on:click={() => showSubsection('certification')}>CERTIFICATION</button>
        <button id="purpose_of_survey-button" on:click={() => showSubsection('purpose_of_survey')}>PURPOSE OF SURVEY</button>
        <button id="circumstances_of_survey-button" on:click={() => showSubsection('circumstances_of_survey')}>CIRCUMSTANCES OF SURVEY</button>
        <button id="report_file_no-button" on:click={() => showSubsection('report_file_no')}>REPORT FILE NO</button>
        <button id="surveyor_qualifications-button" on:click={() => showSubsection('surveyor_qualifications')}>SURVEYOR QUALIFICATIONS</button>
        <button id="intended_use-button" on:click={() => showSubsection('intended_use')}>INTENDED USE</button>
        {#if $project && $project.introduction && $project.introduction.length > 0}
            {#each $project.introduction as subsection}
                    <button on:click={() => showSubsectionStandart('introduction', subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('introduction')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="hull-sections">
        <h1 class="forosnova">Hull sections</h1>
        <button id="layout_overview-button" on:click={() => showSubsection('layout_overview')}>LAYOUT OVERVIEW</button>
        <button id="design-button" on:click={() => showSubsection('design')}>DESIGN</button>
        <button id="deck-button" on:click={() => showSubsection('deck')}>DECK</button>
        <button id="structural_members-button" on:click={() => showSubsection('structural_members')}>STRUCTURAL MEMBERS</button>
        <button id="bottom_paint-button" on:click={() => showSubsection('bottom_paint')}>BOTTOM PAINT</button>
        <button id="blister_comment-button" on:click={() => showSubsection('blister_comment')}>BLISTER COMMENT</button>
        <button id="transom-button" on:click={() => showSubsection('transom')}>TRANSOM</button>
        {#if $project && $project.hull && $project.hull.length > 0}
            {#each $project.hull as subsection}
                <button on:click={() => showSubsectionStandart('hull',subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('hull')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="above-sections">
        <h1 class="forosnova">Above sections</h1>
        <button id="deck_floor_plan-button" on:click={() => showSubsection('deck_floor_plan')}>DECK FLOOR PLAN</button>
        <button id="anchor_platform-button" on:click={() => showSubsection('anchor_platform')}>ANCHOR PLATFORM</button>
        <button id="toe_rails-button" on:click={() => showSubsection('toe_rails')}>TOE RAILS</button>
        <button id="mooring_hardware-button" on:click={() => showSubsection('mooring_hardware')}>MOORING HARDWARE</button>
        <button id="hatches-button" on:click={() => showSubsection('hatches')}>HATCHES</button>
        <button id="exterior_seating-button" on:click={() => showSubsection('exterior_seating')}>EXTERIOR SEATING</button>
        <button id="cockpit_equipment-button" on:click={() => showSubsection('cockpit_equipment')}>COCKPIT EQUIPMENT</button>
        <button id="ngine_hatch-button" on:click={() => showSubsection('ngine_hatch')}>ENGINE HATCH</button>
        <button id="above_draw_water_line-button" on:click={() => showSubsection('above_draw_water_line')}>ABOVE DRAW WATER LINE</button>
        <button id="boarding_ladder-button" on:click={() => showSubsection('boarding_ladder')}>BOARDING LADDER</button>
        <button id="swim_platform-button" on:click={() => showSubsection('swim_platform')}>SWIM PLATFORM</button>
        {#if $project && $project.above && $project.above.length > 0}
            {#each $project.above as subsection}
                <button on:click={() => showSubsectionStandart('above',subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('above')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="below-sections">
        <h1 class="forosnova">Below sections</h1>
        <button id="below_draw_water-button" on:click={() => showSubsection('below_draw_water')}>BELOW DRAW WATER</button>
        <button id="thru_hull_strainers-button" on:click={() => showSubsection('thru_hull_strainers')}>THRU HULL STRAINERS</button>
        <button id="transducer-button" on:click={() => showSubsection('transducer')}>TRANSDUCER(S)</button>
        <button id="sea_valves-button" on:click={() => showSubsection('sea_valves')}>SEA VALVES</button>
        <button id="sea_strainers-button" on:click={() => showSubsection('sea_strainers')}>SEA STRAINERS</button>
        <button id="trim_tabs-button" on:click={() => showSubsection('trim_tabs')}>TRIM TABS</button>
        <button id="note-button" on:click={() => showSubsection('note')}>NOTE</button>
        {#if $project && $project.below && $project.below.length > 0}
            {#each $project.below as subsection}
                <button on:click={() => showSubsectionStandart('below',subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('below')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="cathodic-protection-sections">
        <h1 class="forosnova">Cathodic protection sections</h1>
        <button id="bonding_system-button" on:click={() => showSubsection('bonding_system')}>BONDING SYSTEM</button>
        <button id="anodes-button" on:click={() => showSubsection('anodes')}>ANODES</button>
        <button id="lightning_protection-button" on:click={() => showSubsection('lightning_protection')}>LIGHTNING PROTECTION</button>
        <button id="additional_remarks-button" on:click={() => showSubsection('additional_remarks')}>ADDITIONAL REMARKS</button>
        {#if $project && $project.cathodic && $project.cathodic.length > 0}
            {#each $project.cathodic as subsection}
                <button on:click={() => showSubsectionStandart('cathodic',subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('cathodic')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="helm-station-sections">
        <h1 class="forosnova">Helm station sections</h1>
        <button id="helm_station-button" on:click={() => showSubsection('helm_station')}>HELM STATION</button>
        <button id="throttle_shift_controls-button" on:click={() => showSubsection('throttle_shift_controls')}>THROTTLE & SHIFT CONTROLS</button>
        <button id="engine_room_blowers-button" on:click={() => showSubsection('engine_room_blowers')}>ENGINE ROOM BLOWERS</button>
        <button id="engine_status-button" on:click={() => showSubsection('engine_status')}>ENGINE STATUS</button>
        <button id="other_electronics_controls-button" on:click={() => showSubsection('other_electronics_controls')}>OTHER ELECTRONICS & CONTROLS</button>
        {#if $project && $project.helm && $project.helm.length > 0}
            {#each $project.helm as subsection}
                <button on:click={() => showSubsectionStandart('helm',subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('helm')}>+</button>
    </div>
    <div class="osnova" style="display: none;" id="cabin-interior-sections">
        <h1 class="forosnova">Cabin interior sections</h1>
        <button id="entertainment_berthing-button" on:click={() => showSubsection('entertainment_berthing')}>ENTERTAINMENT BERTHING & SALON</button>
        <button id="interior_lighting-button" on:click={() => showSubsection('interior_lighting')}>INTERIOR LIGHTING</button>
        <button id="galley_dinette-button" on:click={() => showSubsection('galley_dinette')}>GALLEY/DINETTE & ACCESSORIES</button>
        <button id="water_closets-button" on:click={() => showSubsection('water_closets')}>WATER CLOSET(S)</button>
        <button id="climate_control-button" on:click={() => showSubsection('climate_control')}>CLIMATE CONTROL</button>
        {#if $project && $project.cabin && $project.cabin.length > 0}
            {#each $project.cabin as subsection}
                <button on:click={() => showSubsectionStandart('cabin',subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('cabin')}>+</button>
    </div>
    
    <div class="osnova" style="display: none;" id="electrical-systems-sections">
        <h1 class="forosnova">Electrical systems sections</h1>
        <button id="dc_systems_type-button" on:click={() => showSubsection('dc_systems_type')}>DIRECT CURRENT SYSTEM(S) TYPE</button>
        <button id="ac_systems-button" on:click={() => showSubsection('ac_systems')}>ALTERNATING CURRENT (A.C.) SYSTEM(S)</button>
        <button id="generator-button" on:click={() => showSubsection('generator')}>GENERATOR</button>
        {#if $project && $project.electrical && $project.electrical.length > 0}
            {#each $project.electrical as subsection}
                <button on:click={() => showSubsectionStandart('electrical',subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('electrical')}>+</button>
    </div>
    
    <div class="osnova" style="display: none;" id="inboard-propulsion-sections">
        <h1 class="forosnova">Inboard propulsion sections</h1>
        <button id="engines-button" on:click={() => showSubsection('engines')}>ENGINE(S)</button>
        <button id="serial_numbers-button" on:click={() => showSubsection('serial_numbers')}>SERIAL NUMBERS</button>
        <button id="engine_hours-button" on:click={() => showSubsection('engine_hours')}>ENGINE(S) HOURS</button>
        <button id="other_note-button" on:click={() => showSubsection('other_note')}>OTHER NOTE</button>
        <button id="reverse_gears-button" on:click={() => showSubsection('reverse_gears')}>REVERSE GEAR(S)</button>
        <button id="shafting_propellers-button" on:click={() => showSubsection('shafting_propellers')}>SHAFTING & PROPELLER(S)</button>
        {#if $project && $project.inboard && $project.inboard.length > 0}
            {#each $project.inboard as subsection}
                <button on:click={() => showSubsectionStandart('inboard',subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('inboard')}>+</button>
    </div>
    
    <div class="osnova" style="display: none;" id="steering-system-sections">
        <h1 class="forosnova">Steering system sections</h1>
        <button id='manufacture-button' on:click={() => showSubsection('manufacture')}>MANUFACTURE</button>
        <button id='steering_components-button' on:click={() => showSubsection('steering_components')}>STEERING SYSTEM COMPONENTS</button>
        {#if $project && $project.steering && $project.steering.length > 0}
            {#each $project.steering as subsection}
                <button on:click={() => showSubsectionStandart('steering',subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('steering')}>+</button>
    </div>
    
    <div class="osnova" style="display: none;" id="tankage-sections">
        <h1 class="forosnova">Tankage sections</h1>
        <button id='fuel_tank-button' on:click={() => showSubsection('fuel_tank')}>FUEL TANK(S) & PIPING</button>
        <button id='potable_water_system-button' on:click={() => showSubsection('potable_water_system')}>POTABLE WATER SYSTEM & WATER HEATER</button>
        <button id='holding_tank_black_water-button' on:click={() => showSubsection('holding_tank_black_water')}>HOLDING TANK(S)-BLACK WATER</button>
        {#if $project && $project.tankage && $project.tankage.length > 0}
            {#each $project.tankage as subsection}
                <button id='holding_tank_black_water-button' on:click={() => showSubsectionStandart('tankage',subsection.name)}>{subsection.name}</button>
            {/each}
        {/if}
        <button class="forplus" on:click={() => showCreateSubsectionModalStandard('tankage')}>+</button>
    </div>
    
    <div class="osnova" style="display: none;" id="safety-equipment-sections">
        <h1 class="forosnova">Safety equipment sections</h1>
        <button id='navigational_lights-button' on:click={() => showSubsection('navigational_lights')}>NAVIGATIONAL LIGHTS</button>
        <button id='life_jackets-button' on:click={() => showSubsection('life_jackets')}>LIFE JACKETS (P.F.D,'S)</button>
        <button id='throwable_pfd-button' on:click={() => showSubsection('throwable_pfd')}>THROWABLE TYPE P.F.D</button>
        <button id='visual_distress_signals-button' on:click={() => showSubsection('visual_distress_signals')}>VISUAL DISTRESS SIGNALS</button>
        <button id='sound_devices-button' on:click={() => showSubsection('sound_devices')}>SOUND DEVICES</button>
        <button id='uscg_placards-button' on:click={() => showSubsection('uscg_placards')}>U.S.C.G. PLACARDS</button>
        <button id='flame_arrestors-button' on:click={() => showSubsection('flame_arrestors')}>FLAME ARRESTOR(S)</button>
        <button id='engine_ventilation-button' on:click={() => showSubsection('engine_ventilation')}>ENGINE VENTILATION</button>
        <button id='ignition_protection-button' on:click={() => showSubsection('ignition_protection')}>IGNITION PROTECTION</button>
        <button id='inland_navigational_rule_book-button' on:click={() => showSubsection('inland_navigational_rule_book')}>INLAND NAVIGATIONAL RULE BOOK</button>
        <button id='waste_management_plan-button' on:click={() => showSubsection('waste_management_plan')}>WASTE MANAGEMENT PLAN</button>
        <button id='fire_fighting_equipment-button' on:click={() => showSubsection('fire_fighting_equipment')}>FIRE FIGHTING EQUIPMENT</button>
        <button id='bilge_pumps-button' on:click={() => showSubsection('bilge_pumps')}>BILGE PUMPS</button>
        <button id='ground_tackle_windlass-button' on:click={() => showSubsection('ground_tackle_windlass')}>GROUND TACKLE & WINDLASS</button>
        <button id='auxiliary_safety_equipment-button' on:click={() => showSubsection('auxiliary_safety_equipment')}>AUXILIARY SAFETY EQUIPMENT</button>
        {#if $project && $project.safety && $project.safety.length > 0}
            {#each $project.safety as subsection}
                <button on:click={() => showSubsectionStandart('safety',subsection.name)}>{subsection.name}</button>
            {/each}
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

    

    <!--вывод и удаление шага-->
    <!--INTRODUCTION-->
    <div id="gen_info-section" class="infomation" style="display: none;">
        <h2>Gen Info:</h2>
        {#if $project }
            <div>
                <p><strong>City:</strong> { $project.city }</p>
                <p><strong>Phone:</strong> { $project.phone }</p>
                <p><strong>Post:</strong> { $project.post }</p>
                <p><strong>vessel name:</strong> { $project.vessel_name }</p>
            </div>
        {/if}
        
        {#if $project && $project.gen_info_steps && $project.gen_info_steps.length > 0}
            <ul>
                {#each $project.gen_info_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('gen_info', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="gen_info" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--certification -->
    <div id="certification-section" style="display: none;" class="infomation">
        <h2>certification:</h2>
        {#if $project && $project.certification_steps && $project.certification_steps.length > 0}
            <ul>
                {#each $project.certification_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('certification', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="certification" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- purpose_of_survey-section -->
    <div id="purpose_of_survey-section" style="display: none;" class="infomation">
        <h2>purpose of survey:</h2>
        {#if $project && $project.purpose_of_survey_steps && $project.purpose_of_survey_steps.length > 0}
            <ul>
                {#each $project.purpose_of_survey_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('purpose_of_survey', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="purpose_of_survey" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- purpose_of_survey-section -->
    <div id="circumstances_of_survey-section" style="display: none;" class="infomation">
        <h2>circumstances of survey:</h2>
        {#if $project && $project.circumstances_of_survey_steps && $project.circumstances_of_survey_steps.length > 0}
            <ul>
                {#each $project.circumstances_of_survey_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('circumstances_of_survey', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="circumstances_of_survey" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- report_file_no-section -->
    <div id="report_file_no-section" style="display: none;" class="infomation">
        <h2>report file no:</h2>
        {#if $project && $project.report_file_no_steps && $project.report_file_no_steps.length > 0}
            <ul>
                {#each $project.report_file_no_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('report_file_no', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="report_file_no" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- surveyor_qualifications-section -->
    <div id="surveyor_qualifications-section" style="display: none;" class="infomation">
        <h2>surveyor qualifications</h2>
        {#if $project && $project.surveyor_qualifications_steps && $project.surveyor_qualifications_steps.length > 0}
            <ul>
                {#each $project.surveyor_qualifications_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('surveyor_qualifications', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="surveyor_qualifications" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- intended_use-section -->
    <div id="intended_use-section" style="display: none;" class="infomation">
        <h2>intended use</h2>
        {#if $project && $project.intended_use_steps && $project.intended_use_steps.length > 0}
            <ul>
                {#each $project.intended_use_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('intended_use', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="intended_use" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Hull, DECK & SUPERSTRUCTURE-->
    <!-- layout_overview-section -->
    <div id="layout_overview-section" style="display: none;" class="infomation">
        <h2>layout overview</h2>
        {#if $project && $project.layout_overview_steps && $project.layout_overview_steps.length > 0}
            <ul>
                {#each $project.layout_overview_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('layout_overview', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="layout_overview" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- design-section -->
    <div id="design-section" style="display: none;" class="infomation">
        <h2>design</h2>
        {#if $project && $project.design_steps && $project.design_steps.length > 0}
            <ul>
                {#each $project.design_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('design', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="design" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- deck-section -->
    <div id="deck-section" style="display: none;" class="infomation">
        <h2>deck</h2>
        {#if $project && $project.deck_steps && $project.deck_steps.length > 0}
            <ul>
                {#each $project.deck_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('deck', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="deck" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- structural_members-section -->
    <div id="structural_members-section" style="display: none;" class="infomation">
        <h2>structural_members</h2>
        {#if $project && $project.structural_members_steps && $project.structural_members_steps.length > 0}
            <ul>
                {#each $project.structural_members_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('structural_members', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="structural_members" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- bottom_paint-section -->
    <div id="bottom_paint-section" style="display: none;" class="infomation">
        <h2>bottom_paint</h2>
        {#if $project && $project.bottom_paint_steps && $project.bottom_paint_steps.length > 0}
            <ul>
                {#each $project.bottom_paint_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('bottom_paint', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="bottom_paint" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- blister_comment-section -->
    <div id="blister_comment-section" style="display: none;" class="infomation">
        <h2>blister_comment</h2>
        {#if $project && $project.blister_comment_steps && $project.blister_comment_steps.length > 0}
            <ul>
                {#each $project.blister_comment_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('blister_comment', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="blister_comment" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- transom-section -->
    <div id="transom-section" style="display: none;" class="infomation">
        <h2>transom</h2>
        {#if $project && $project.transom_steps && $project.transom_steps.length > 0}
            <ul>
                {#each $project.transom_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('transom', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="transom" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Above-->
    <!-- deck_floor_plan-section -->
    <div id="deck_floor_plan-section" style="display: none;" class="infomation">
        <h2>deck floor plan</h2>
        {#if $project && $project.deck_floor_plan_steps && $project.deck_floor_plan_steps.length > 0}
            <ul>
                {#each $project.deck_floor_plan_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('deck_floor_plan', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="deck_floor_plan" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- anchor_platform-section -->
    <div id="anchor_platform-section" style="display: none;" class="infomation">
        <h2>anchor platform</h2>
        {#if $project && $project.anchor_platform_steps && $project.anchor_platform_steps.length > 0}
            <ul>
                {#each $project.anchor_platform_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('anchor_platform', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="anchor_platform" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- toe_rails-section -->
    <div id="toe_rails-section" style="display: none;" class="infomation">
        <h2>toe rails</h2>
        {#if $project && $project.toe_rails_steps && $project.toe_rails_steps.length > 0}
            <ul>
                {#each $project.toe_rails_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('toe_rails', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="toe_rails" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- mooring_hardware-section -->
    <div id="mooring_hardware-section" style="display: none;" class="infomation">
        <h2>mooring hardware</h2>
        {#if $project && $project.mooring_hardware_steps && $project.mooring_hardware_steps.length > 0}
            <ul>
                {#each $project.mooring_hardware_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('mooring_hardware', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="mooring_hardware" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- hatches-section -->
    <div id="hatches-section" style="display: none;" class="infomation">
        <h2>hatches</h2>
        {#if $project && $project.hatches_steps && $project.hatches_steps.length > 0}
            <ul>
                {#each $project.hatches_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('hatches', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="hatches" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- exterior_seating-section -->
    <div id="exterior_seating-section" style="display: none;" class="infomation">
        <h2>exterior seating</h2>
        {#if $project && $project.exterior_seating_steps && $project.exterior_seating_steps.length > 0}
            <ul>
                {#each $project.exterior_seating_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('exterior_seating', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="exterior_seating" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- cockpit_equipment-section -->
    <div id="cockpit_equipment-section" style="display: none;" class="infomation">
        <h2>cockpit equipment</h2>
        {#if $project && $project.cockpit_equipment_steps && $project.cockpit_equipment_steps.length > 0}
            <ul>
                {#each $project.cockpit_equipment_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('cockpit_equipment', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="cockpit_equipment" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!-- ngine_hatch-section -->
    <div id="ngine_hatch-section" style="display: none;" class="infomation">
        <h2>ngine hatch</h2>
        {#if $project && $project.ngine_hatch_steps && $project.ngine_hatch_steps.length > 0}
            <ul>
                {#each $project.ngine_hatch_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('ngine_hatch', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="ngine_hatch" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--above_draw_water_line-section -->
    <div id="above_draw_water_line-section" style="display: none;" class="infomation">
        <h2>above draw water line</h2>
        {#if $project && $project.above_draw_water_line_steps && $project.above_draw_water_line_steps.length > 0}
            <ul>
                {#each $project.above_draw_water_line_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('above_draw_water_line', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="above_draw_water_line" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--boarding_ladder-section -->
    <div id="boarding_ladder-section" style="display: none;" class="infomation">
        <h2>boarding ladder</h2>
        {#if $project && $project.boarding_ladder_steps && $project.boarding_ladder_steps.length > 0}
            <ul>
                {#each $project.boarding_ladder_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('boarding_ladder', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="boarding_ladder" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--swim_platform-section -->
    <div id="swim_platform-section" style="display: none;" class="infomation">
        <h2>swim platformt</h2>
        {#if $project && $project.swim_platform_steps && $project.swim_platform_steps.length > 0}
            <ul>
                {#each $project.swim_platform_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('swim_platform', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="swim_platform" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Below -->
    <!--below_draw_water-section -->
    <div id="below_draw_water-section" style="display: none;" class="infomation">
        <h2>below draw water</h2>
        {#if $project && $project.below_draw_water_steps && $project.below_draw_water_steps.length > 0}
            <ul>
                {#each $project.below_draw_water_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('below_draw_water', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="below_draw_water" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--thru_hull_strainers-section -->
    <div id="thru_hull_strainers-section" style="display: none;" class="infomation">
        <h2>sthru hull strainers</h2>
        {#if $project && $project.thru_hull_strainers_steps && $project.thru_hull_strainers_steps.length > 0}
            <ul>
                {#each $project.thru_hull_strainers_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('thru_hull_strainers', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="thru_hull_strainers" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--transducer-section -->
    <div id="transducer-section" style="display: none;" class="infomation">
        <h2>transducer</h2>
        {#if $project && $project.transducer_steps && $project.transducer_steps.length > 0}
            <ul>
                {#each $project.transducer_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('transducer', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="transducer" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--sea_valves-section -->
    <div id="sea_valves-section" style="display: none;" class="infomation">
        <h2>sea valves</h2>
        {#if $project && $project.sea_valves_steps && $project.sea_valves_steps.length > 0}
            <ul>
                {#each $project.sea_valves_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('sea_valves', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="sea_valves" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--sea_strainers-section -->
    <div id="sea_strainers-section" style="display: none;" class="infomation">
        <h2>sea strainers</h2>
        {#if $project && $project.sea_strainers_steps && $project.sea_strainers_steps.length > 0}
            <ul>
                {#each $project.sea_strainers_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('sea_strainers', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="sea_strainers" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--trim_tabs-section -->
    <div id="trim_tabs-section" style="display: none;" class="infomation">
        <h2>trim tabs</h2>
        {#if $project && $project.trim_tabs_steps && $project.trim_tabs_steps.length > 0}
            <ul>
                {#each $project.trim_tabs_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('trim_tabs', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="trim_tabs" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--note-section -->
    <div id="note-section" style="display: none;" class="infomation">
        <h2>note</h2>
        {#if $project && $project.note_steps && $project.note_steps.length > 0}
            <ul>
                {#each $project.note_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('note', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="note" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--bonding_system-section -->
    <div id="bonding_system-section" style="display: none;" class="infomation">
        <h2>bonding system</h2>
        {#if $project && $project.bonding_system_steps && $project.bonding_system_steps.length > 0}
            <ul>
                {#each $project.bonding_system_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('bonding_system', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="bonding_system" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--anodes-section -->
    <div id="anodes-section" style="display: none;" class="infomation">
        <h2>anodes</h2>
        {#if $project && $project.anodes_steps && $project.anodes_steps.length > 0}
            <ul>
                {#each $project.anodes_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('anodes', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="anodes" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--lightning_protection-section -->
    <div id="lightning_protection-section" style="display: none;" class="infomation">
        <h2>lightning protection</h2>
        {#if $project && $project.lightning_protection_steps && $project.lightning_protection_steps.length > 0}
            <ul>
                {#each $project.lightning_protection_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('lightning_protection', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="lightning_protection" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--additional_remarks-section -->
    <div id="additional_remarks-section" style="display: none;" class="infomation">
        <h2>additional remarks</h2>
        {#if $project && $project.additional_remarks_steps && $project.additional_remarks_steps.length > 0}
            <ul>
                {#each $project.additional_remarks_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('additional_remarks', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="additional_remarks" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Helm-->
    <!--helm_station-section -->
    <div id="helm_station-section" style="display: none;" class="infomation">
        <h2>helm station</h2>
        {#if $project && $project.helm_station_steps && $project.helm_station_steps.length > 0}
            <ul>
                {#each $project.helm_station_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('helm_station', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="helm_station" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--throttle_shift_controls-section -->
    <div id="throttle_shift_controls-section" style="display: none;" class="infomation">
        <h2>throttle shift controls</h2>
        {#if $project && $project.throttle_shift_controls_steps && $project.throttle_shift_controls_steps.length > 0}
            <ul>
                {#each $project.throttle_shift_controls_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('throttle_shift_controls', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="throttle_shift_controls" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--engine_room_blowers-section -->
    <div id="engine_room_blowers-section" style="display: none;" class="infomation">
        <h2>engine room blowers</h2>
        {#if $project && $project.engine_room_blowers_steps && $project.engine_room_blowers_steps.length > 0}
            <ul>
                {#each $project.engine_room_blowers_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('engine_room_blowers', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="engine_room_blowers" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--engine_status-section -->
    <div id="engine_status-section" style="display: none;" class="infomation">
        <h2>engine status</h2>
        {#if $project && $project.engine_status_steps && $project.engine_status_steps.length > 0}
            <ul>
                {#each $project.engine_status_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('engine_status', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="engine_status" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--other_electronics_controls-section -->
    <div id="other_electronics_controls-section" style="display: none;" class="infomation">
        <h2>other electronics controls</h2>
        {#if $project && $project.other_electronics_controls_steps && $project.other_electronics_controls_steps.length > 0}
            <ul>
                {#each $project.other_electronics_controls_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('other_electronics_controls', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="other_electronics_controls" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Cabin-->
    <!--entertainment_berthing-section -->
    <div id="entertainment_berthing-section" style="display: none;" class="infomation">
        <h2>other electronics controls</h2>
        {#if $project && $project.entertainment_berthing_steps && $project.entertainment_berthing_steps.length > 0}
            <ul>
                {#each $project.entertainment_berthing_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('entertainment_berthing', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="entertainment_berthing" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--interior_lighting-section -->
    <div id="interior_lighting-section" style="display: none;" class="infomation">
        <h2>interior lighting</h2>
        {#if $project && $project.interior_lighting_steps && $project.interior_lighting_steps.length > 0}
            <ul>
                {#each $project.interior_lighting_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('interior_lighting', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="interior_lighting" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--galley_dinette-section -->
    <div id="galley_dinette-section" style="display: none;" class="infomation">
        <h2>galley dinette</h2>
        {#if $project && $project.galley_dinette_steps && $project.galley_dinette_steps.length > 0}
            <ul>
                {#each $project.galley_dinette_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('galley_dinette', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="galley_dinette" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--water_closets-section -->
    <div id="water_closets-section" style="display: none;" class="infomation">
        <h2>water closets</h2>
        {#if $project && $project.water_closets_steps && $project.water_closets_steps.length > 0}
            <ul>
                {#each $project.water_closets_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('water_closets', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="water_closets" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--climate_control-section -->
    <div id="climate_control-section" style="display: none;" class="infomation">
        <h2>climate control</h2>
        {#if $project && $project.climate_control_steps && $project.climate_control_steps.length > 0}
            <ul>
                {#each $project.climate_control_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('climate_control', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="climate_control" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Electric controp-->
    <!--dc_systems_type-section -->
    <div id="dc_systems_type-section" style="display: none;" class="infomation">
        <h2>dc systems type</h2>
        {#if $project && $project.dc_systems_type_steps && $project.dc_systems_type_steps.length > 0}
            <ul>
                {#each $project.dc_systems_type_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('dc_systems_type', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="dc_systems_type" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--ac_systems-section -->
    <div id="ac_systems-section" style="display: none;" class="infomation">
        <h2>ac systems</h2>
        {#if $project && $project.ac_systems_steps && $project.ac_systems_steps.length > 0}
            <ul>
                {#each $project.ac_systems_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('ac_systems', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="ac_systems" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--generator-section -->
    <div id="generator-section" style="display: none;" class="infomation">
        <h2>generator</h2>
        {#if $project && $project.generator_steps && $project.generator_steps.length > 0}
            <ul>
                {#each $project.generator_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('generator', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="generator" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Inboard-->
    <!--engines-section -->
    <div id="engines-section" style="display: none;" class="infomation">
        <h2>engines</h2>
        {#if $project && $project.engines_steps && $project.engines_steps.length > 0}
            <ul>
                {#each $project.engines_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('engines', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="engines" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--serial_numbers-section -->
    <div id="serial_numbers-section" style="display: none;" class="infomation">
        <h2>serial numbers</h2>
        {#if $project && $project.serial_numbers_steps && $project.serial_numbers_steps.length > 0}
            <ul>
                {#each $project.serial_numbers_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('serial_numbers', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="serial_numbers" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--engine_hours-section -->
    <div id="engine_hours-section" style="display: none;" class="infomation">
        <h2>engine hours</h2>
        {#if $project && $project.engine_hours_steps && $project.engine_hours_steps.length > 0}
            <ul>
                {#each $project.engine_hours_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('engine_hours', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="engine_hours" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--other_note-section -->
    <div id="other_note-section" style="display: none;" class="infomation">
        <h2>other note</h2>
        {#if $project && $project.other_note_steps && $project.other_note_steps.length > 0}
            <ul>
                {#each $project.other_note_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('other_note', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="other_note" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--reverse_gears-section -->
    <div id="reverse_gears-section" style="display: none;" class="infomation">
        <h2>reverse gears</h2>
        {#if $project && $project.reverse_gears_steps && $project.reverse_gears_steps.length > 0}
            <ul>
                {#each $project.reverse_gears_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('reverse_gears', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="reverse_gears" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--shafting_propellers-section -->
    <div id="shafting_propellers-section" style="display: none;" class="infomation">
        <h2>shafting propellers</h2>
        {#if $project && $project.shafting_propellers_steps && $project.shafting_propellers_steps.length > 0}
            <ul>
                {#each $project.shafting_propellers_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('shafting_propellers', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="shafting_propellers" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Streeng-->
    <!--manufacture-section -->
    <div id="manufacture-section" style="display: none;" class="infomation">
        <h2>manufacture</h2>
        {#if $project && $project.manufacture_steps && $project.manufacture_steps.length > 0}
            <ul>
                {#each $project.manufacture_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('manufacture', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="manufacture" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--steering_components-section -->
    <div id="steering_components-section" style="display: none;" class="infomation">
        <h2>msteering components</h2>
        {#if $project && $project.steering_components_steps && $project.steering_components_steps.length > 0}
            <ul>
                {#each $project.steering_components_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('steering_components', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="steering_components" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Tankage-->
    <!--fuel_tank-section -->
    <div id="fuel_tank-section" style="display: none;" class="infomation">
        <h2>fuel tank</h2>
        {#if $project && $project.fuel_tank_steps && $project.fuel_tank_steps.length > 0}
            <ul>
                {#each $project.fuel_tank_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('fuel_tank', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="fuel_tank" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--potable_water_system-section -->
    <div id="potable_water_system-section" style="display: none;" class="infomation">
        <h2>potable water system</h2>
        {#if $project && $project.potable_water_system_steps && $project.potable_water_system_steps.length > 0}
            <ul>
                {#each $project.potable_water_system_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('potable_water_system', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="potable_water_system" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--holding_tank_black_water-section -->
    <div id="holding_tank_black_water-section" style="display: none;" class="infomation">
        <h2>holding tank black water</h2>
        {#if $project && $project.holding_tank_black_water_steps && $project.holding_tank_black_water_steps.length > 0}
            <ul>
                {#each $project.holding_tank_black_water_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('holding_tank_black_water', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="holding_tank_black_water" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Safety-->
    <!--navigational_lights-section -->
    <div id="navigational_lights-section" style="display: none;" class="infomation">
        <h2>navigational lights</h2>
        {#if $project && $project.navigational_lights_steps && $project.navigational_lights_steps.length > 0}
            <ul>
                {#each $project.navigational_lights_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('navigational_lights', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="navigational_lights" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--life_jackets-section -->
    <div id="life_jackets-section" style="display: none;" class="infomation">
        <h2>life jackets</h2>
        {#if $project && $project.life_jackets_steps && $project.life_jackets_steps.length > 0}
            <ul>
                {#each $project.life_jackets_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('life_jackets', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="life_jackets" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--throwable_pfd-section -->
    <div id="throwable_pfd-section" style="display: none;" class="infomation">
        <h2>throwable pfd</h2>
        {#if $project && $project.throwable_pfd_steps && $project.throwable_pfd_steps.length > 0}
            <ul>
                {#each $project.throwable_pfd_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('throwable_pfd', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="throwable_pfd" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--visual_distress_signals-section -->
    <div id="visual_distress_signals-section" style="display: none;" class="infomation">
        <h2>visual distress signals</h2>
        {#if $project && $project.visual_distress_signals_steps && $project.visual_distress_signals_steps.length > 0}
            <ul>
                {#each $project.visual_distress_signals_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('visual_distress_signals', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="visual_distress_signals" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--sound_devices-section -->
    <div id="sound_devices-section" style="display: none;" class="infomation">
        <h2>sound devices</h2>
        {#if $project && $project.sound_devices_steps && $project.sound_devices_steps.length > 0}
            <ul>
                {#each $project.sound_devices_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('sound_devices', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="sound_devices" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--uscg_placards-section -->
    <div id="uscg_placards-section" style="display: none;" class="infomation">
        <h2>uscg placards</h2>
        {#if $project && $project.uscg_placards_steps && $project.uscg_placards_steps.length > 0}
            <ul>
                {#each $project.uscg_placards_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('uscg_placards', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="uscg_placards" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--flame_arrestors-section -->
    <div id="flame_arrestors-section" style="display: none;" class="infomation">
        <h2>flame arrestors</h2>
        {#if $project && $project.flame_arrestors_steps && $project.flame_arrestors_steps.length > 0}
            <ul>
                {#each $project.flame_arrestors_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('flame_arrestors', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="flame_arrestors" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--engine_ventilation-section -->
    <div id="engine_ventilation-section" style="display: none;" class="infomation">
        <h2>engine ventilation</h2>
        {#if $project && $project.engine_ventilation_steps && $project.engine_ventilation_steps.length > 0}
            <ul>
                {#each $project.engine_ventilation_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('engine_ventilation', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="engine_ventilation" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--ignition_protection-section -->
    <div id="ignition_protection-section" style="display: none;" class="infomation">
        <h2>ignition protection</h2>
        {#if $project && $project.ignition_protection_steps && $project.ignition_protection_steps.length > 0}
            <ul>
                {#each $project.ignition_protection_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('ignition_protection', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="ignition_protection" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--inland_navigational_rule_book-section -->
    <div id="inland_navigational_rule_book-section" style="display: none;" class="infomation">
        <h2>inland navigational rule book</h2>
        {#if $project && $project.inland_navigational_rule_book_steps && $project.inland_navigational_rule_book_steps.length > 0}
            <ul>
                {#each $project.inland_navigational_rule_book_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('inland_navigational_rule_book', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="inland_navigational_rule_book" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--waste_management_plan-section -->
    <div id="waste_management_plan-section" style="display: none;" class="infomation">
        <h2>waste management plan</h2>
        {#if $project && $project.waste_management_plan_steps && $project.waste_management_plan_steps.length > 0}
            <ul>
                {#each $project.waste_management_plan_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('waste_management_plan', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="waste_management_plan" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--fire_fighting_equipment-section -->
    <div id="fire_fighting_equipment-section" style="display: none;" class="infomation">
        <h2>fire fighting equipment</h2>
        {#if $project && $project.fire_fighting_equipment_steps && $project.fire_fighting_equipment_steps.length > 0}
            <ul>
                {#each $project.fire_fighting_equipment_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('fire_fighting_equipment', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="fire_fighting_equipment" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--bilge_pumps-section -->
    <div id="bilge_pumps-section" style="display: none;" class="infomation">
        <h2>bilge pumps</h2>
        {#if $project && $project.bilge_pumps_steps && $project.bilge_pumps_steps.length > 0}
            <ul>
                {#each $project.bilge_pumps_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('bilge_pumps', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="bilge_pumps" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--ground_tackle_windlass-section -->
    <div id="ground_tackle_windlass-section" style="display: none;" class="infomation">
        <h2>ground tackle windlass</h2>
        {#if $project && $project.ground_tackle_windlass_steps && $project.ground_tackle_windlass_steps.length > 0}
            <ul>
                {#each $project.ground_tackle_windlass_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('ground_tackle_windlass', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="ground_tackle_windlass" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--auxiliary_safety_equipment-section -->
    <div id="auxiliary_safety_equipment-section" style="display: none;" class="infomation">
        <h2>auxiliary safety equipment</h2>
        {#if $project && $project.auxiliary_safety_equipment_steps && $project.auxiliary_safety_equipment_steps.length > 0}
            <ul>
                {#each $project.auxiliary_safety_equipment_steps as step}
                    <li>{step}</li>
                    <form on:submit|preventDefault={() => deleteStep('auxiliary_safety_equipment', step)}>
                        <input type="hidden" name="step_to_delete" value={step} />
                        <input type="hidden" name="section" value="auxiliary_safety_equipment" />
                        <button type="submit">Delete</button>
                    </form>
                {/each}
            </ul>
        {:else}
            <p>No steps added yet.</p>
        {/if}
    </div>
    <!--Добавление шага-->
    <div id="add-step-form-container" style="display: none;">
        <h2>Add Step:</h2>
        <form on:submit={addStep}><!--<form method="POST" action="/edit_project/{{ project_id }}/add_step">-->
            <label for="step_description">Step Description:</label>
            <input type="text" id="step_description" name="step_description">
            
            <input type="hidden" name="section" id="current_section" value="">
            <button type="submit">Add Step</button>
        </form>
    </div>
    
    <!--Добавление шага стандартные разделы-->
    <div id="add-step-form-container_standard" style="display: none;">
        <h2>Add Step standard:</h2>
        {#if $project && $project[currentSection] && $project[currentSection].length > 0}
            {#each $project[currentSection] as subsection}
                <div>
                    {#if openedSubsection === subsection.name}
                        {#if subsection.subsections && subsection.subsections.length > 0}
                            <ul>
                                {#each subsection.subsections as step}
                                    <li>{step.step_description}</li>
                                {/each}
                            </ul>
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
    </div>
</main>