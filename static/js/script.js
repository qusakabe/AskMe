    document.addEventListener("DOMContentLoaded", function () {
    const imageUpload = document.getElementById("image-upload");
    const profileImagePreview = document.getElementById("profile-image-preview");

    if (imageUpload) {
        imageUpload.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    profileImagePreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    const login = document.querySelector('.small-input-container[placeholder="Write login"]');
    const email = document.querySelector('.small-input-container[placeholder="Write email"]');
    const password = document.querySelector('.small-input-container[placeholder="Write password"]');
    const repeatPassword = document.querySelector('.small-input-container[placeholder="Repeat password"]');

    const inputs = [
        { field: login, errorId: "login-error", validate: validateLogin },
        { field: email, errorId: "email-error", validate: validateEmail },
        { field: password, errorId: "password-error", validate: validatePassword },
        { field: repeatPassword, errorId: "repeat-password-error", validate: validateRepeatPassword },
    ];

    inputs.forEach(({ field, validate }) => {
        if (field) {
            field.addEventListener("input", validate);
            field.addEventListener("blur", validate);
        }
    });

    function validateLogin() {
        checkField(login, "login-error", login.value.trim() !== "", "Login is required");
    }

    function validateEmail() {
        const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
        checkField(email, "email-error", isValid, "Valid email is required");
    }

    function validatePassword() {
        checkField(password, "password-error", password.value.length >= 8, "Password must be at least 8 characters");
    }

    function validateRepeatPassword() {
        checkField(repeatPassword, "repeat-password-error", repeatPassword.value === password.value, "Passwords do not match");
    }

    function checkField(input, errorId, condition, message) {
        const errorElement = document.getElementById(errorId);
        if (condition) {
            errorElement.textContent = "";
            input.classList.remove("error");
        } else {
            errorElement.textContent = message;
            input.classList.add("error");
        }
    }
});

function validateNewquestion(){
    let valid = true;

    const title = document.getElementById('question-title');
    const title_error = document.getElementById('question-title-error');

    const text = document.getElementById("question-text");
    const text_error = document.getElementById("question-text-error");

    const tags = document.getElementById("tags");
    const tags_error = document.getElementById("tags-input-error");


    if (title.value.trim().length < 10){
        title_error.textContent = "Your title is shorter than 10 characters.";
        title.classList.add("error");
        valid = false;
    } else if(title.value.trim().length > 100){
        title_error.textContent = "Your title is longer than 100 characters.";
        title.classList.add("error");
        valid = false;
    } else {
        title_error.textContent = ""
        title.classList.remove("error");
    }

    if (text.value.trim().length < 10){
        text_error.textContent = "Your text is shorter than 10 characters.";
        text.classList.add("error");
        valid = false;
    } else if(text.value.trim().length > 5000){
        text_error.textContent = "Your text is longer than 5000 characters.";
        text.classList.add("error");
        valid = false;
    } else {
        text_error.textContent = ""
        text.classList.remove("error");
    }

    if (tags.value.trim().length > 60){
        tags_error.textContent = "Your tags are too long.";
        tags.classList.add("error");
        valid = false;
    } else {
        tags_error.textContent = "";
        tags.classList.remove("error");
    }


    return valid;
}


function validateAnswer(){
    let valid = true;
    const input_data = document.getElementById("answer-input");
    const error = document.getElementById("new-answer-error");

    if (input_data.value.trim().length < 40){
        error.textContent = "Your answer is shorter than 40 characters.";
        input_data.classList.add("error");
        valid = false;
    } else if(input_data.value.trim().length > 1000){
        error.textContent = "Your answer is longer than 1000 characters.";
        input_data.classList.add("error");
        valid = false;
    } else {
        error.textContent = ""
        input_data.classList.remove("error");
    }
    return valid;
}


const ratingBoxes = document.querySelectorAll('.raiting-box');

ratingBoxes.forEach((ratingBox) => {
    const likeButton = ratingBox.querySelector('.like-button');
    const dislikeButton = ratingBox.querySelector('.dislike-button');
    const counter = ratingBox.querySelector('.raiting-counter');

    let likeActive = false;
    let dislikeActive = false;
    let count = parseInt(counter.textContent.trim());

    likeButton.addEventListener('mouseenter', () => {
        if (!likeActive) {
            ratingBox.classList.add('green');
        }
    });
    likeButton.addEventListener('mouseleave', () => {
        if (!likeActive) {
            ratingBox.classList.remove('green');
        }
    });

    dislikeButton.addEventListener('mouseenter', () => {
        if (!dislikeActive) {
            ratingBox.classList.add('red');
        }
    });
    dislikeButton.addEventListener('mouseleave', () => {
        if (!dislikeActive) {
            ratingBox.classList.remove('red');
        }
    });

    likeButton.addEventListener('click', () => {
        if (likeActive) {
            likeActive = false;
            ratingBox.classList.remove('green');
            count--;
        } else {
            likeActive = true;
            ratingBox.classList.add('green');
            if (dislikeActive) {
                dislikeActive = false;
                ratingBox.classList.remove('red');
                count++;
            }
            count++;
        }
        updateCounter();
    });

    dislikeButton.addEventListener('click', () => {
        if (dislikeActive) {
            dislikeActive = false;
            ratingBox.classList.remove('red');
            count++;
        } else {
            dislikeActive = true;
            ratingBox.classList.add('red');
            if (likeActive) {
                likeActive = false;
                ratingBox.classList.remove('green');
                count--;
            }
            count--;
        }
        updateCounter();
    });

    function updateCounter() {
        counter.textContent = count;
    }
});


const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");
const pagesContainer = document.getElementById("pages-container");
const paginationElement = document.querySelector(".pagination"); // Исправлено на querySelector





const urlParams = new URLSearchParams(window.location.search);
let currentPage = Number(urlParams.get('page')) || 1;

const maxVisiblePages = 5; // Количество отображаемых страниц

if (pagesContainer) {
    const totalItems = Number(paginationElement.getAttribute('data-total-items')) || 0;
    const totalPages = Math.max(1, Math.ceil(totalItems / 10)); // Количество страниц
    renderPages();

        function renderPages() {
        pagesContainer.innerHTML = "";

        let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
        let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
        console.log("start: ",startPage);
        console.log("end: ",endPage);

        if (endPage === totalPages) {
            startPage = Math.max(1, totalPages - maxVisiblePages + 1);
        }

        if (startPage > 1) {
            createPage(1);
            if (startPage > 2) createDots();
        }

        for (let i = startPage; i <= endPage; i++) {
            createPage(i, i === currentPage);
        }

        if (endPage < totalPages - 1) {
            createDots();
        }

        if (endPage < totalPages) {
            createPage(totalPages);
        }

        if (prevButton) {
            prevButton.classList.toggle("disabled", currentPage === 1);
        }

        if (nextButton) {
            nextButton.classList.toggle("disabled", currentPage === totalPages);
        }

    }

    function createPage(number, isActive = false) {
        const page = document.createElement("a");
        page.href = `?page=${number}`;
        page.classList.add("page");
        page.textContent = number;

        if (isActive) {
            page.classList.add("active");
        }

        page.addEventListener("click", () => {
            window.location.href = `?page=${number}`;
        });

        pagesContainer.appendChild(page);
    }

    function createDots() {
        const dots = document.createElement("span");
        dots.classList.add("dots");
        dots.textContent = "...";
        pagesContainer.appendChild(dots);
    }

    if (prevButton) {
        prevButton.addEventListener("click", (e) => {
            e.preventDefault();
            if (currentPage > 1) {
                window.location.href = `?page=${currentPage - 1}`;
            }
        });
    }

    if (nextButton) {
        nextButton.addEventListener("click", (e) => {
            e.preventDefault();
            if (currentPage < totalPages) {
                window.location.href = `?page=${currentPage + 1}`;
            }
        });
    }
}

// Массив доступных тегов
const availableTags = [
    "HTML", "CSS", "JavaScript", "jQuery", "React", "Angular", "Vue",
    "Node.js", "PHP", "Python", "Django", "Flask", "Java", "Spring",
    "C#", ".NET", "Swift", "Kotlin", "SQL", "MongoDB", "TypeScript"
];

const tagInput = document.getElementById("tags");

if (tagInput) { // Только если инпут есть на странице
    $("#tags").autocomplete({
        source: function(request, response) {
            let currentValue = request.term;
            let lastTag = currentValue.split(',').pop().trim(); // Получаем последний введенный тег

            if (lastTag === "") return; // Если последний тег пустой — не показываем подсказки

            let filteredTags = availableTags.filter(tag => 
                tag.toLowerCase().startsWith(lastTag.toLowerCase())
            );

            response(filteredTags);
        },
        minLength: 1,
        focus: function(event, ui) {
            event.preventDefault(); // Предотвращаем замену всего текста при наведении стрелками
        },
        select: function(event, ui) {
            let currentValue = $("#tags").val();
            let tags = currentValue.split(',').map(tag => tag.trim()).filter(tag => tag !== ""); 

            if (tags.length > 0) {
                tags.pop();
            }

            if (tags.length < 3 && !tags.includes(ui.item.value)) {
                tags.push(ui.item.value);
            }

            $("#tags").val(tags.join(", ") + (tags.length < 3 ? ", " : ""));        
            event.preventDefault();
        },
        open: function() {
            let autocompleteMenu = $(".ui-autocomplete");
            let inputOffset = $("#tags").offset();
            let inputHeight = $("#tags").outerHeight();

            autocompleteMenu.css({
                "top": (inputOffset.top + inputHeight - 2) + "px",
                "left": inputOffset.left + "px"
            });
        }
    });

    tagInput.addEventListener("focus", function () {    
        initAutocomplete();
    });

    tagInput.addEventListener("input", function () {
        initAutocomplete();
    });

    tagInput.addEventListener("keyup", function(event) {
        let currentValue = tagInput.value;
        let tags = currentValue.split(',').map(tag => tag.trim()).filter(tag => tag !== "");

        if (tags.length > 3) {
            tagInput.value = tags.slice(0, 3).join(", ") + ", ";
        }
    });

    const autocompleteItems = document.getElementsByClassName('ui-autocomplete');
    for (const autocompleteItem of autocompleteItems) {
        autocompleteItem.style = 'margin-top: 10px;';
    }
}

document.querySelectorAll('.correct-button').forEach(button => {
    let correctFlag = false;
    
    button.addEventListener('click', () => {
        const checkIcon = button.querySelector('.correct-icon');

        if (correctFlag) {
            button.classList.remove("correct");
            button.textContent = "mark correct";
            button.appendChild(checkIcon); // Вернуть иконку в кнопку
            checkIcon.style.display = "none";
            correctFlag = false;
        } else {
            button.classList.add("correct");
            button.textContent = "correct";
            button.insertBefore(checkIcon, button.firstChild); // Переместить иконку в начало
            checkIcon.style.display = "block";
            correctFlag = true;
        }
    });
});