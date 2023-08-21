let gameTimer;
const wordInput = document.querySelector('input[name="word"]');  // Define wordInput within the function scope

function startGameTimer() {
    gameTimer = setTimeout(disableForm, 60000);
}

function submitWord(event) {
    event.preventDefault();

    const submitButton = document.querySelector('form button[type="submit"]');

    if (!submitButton.disabled && wordInput.value.trim() !== '') {
        const word = wordInput.value.toUpperCase();

        axios.post('/check_word', { word: word })
            .then(response => {
                displayResult(response.data.result);
                if (response.data.result === 'ok') {
                    const scoreDisplay = document.getElementById('score-display');
                    scoreDisplay.textContent = parseInt(scoreDisplay.textContent) + word.length;
                    postStats(word.length);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });

        wordInput.value = '';
    }
}

function disableForm() {
    const submitButton = document.querySelector('form button[type="submit"]');
    submitButton.disabled = true;
}

function postStats(score) {
    axios.post('/update_stats', { score: score })
        .then(response => {
            console.log('Stats updated:', response.data);
        })
        .catch(error => {
            console.log('Error:', error);
        });
}

function displayResult(result) {
    const resultMessage = document.getElementById('result-message');
    const scoreDisplay = document.getElementById('score-display');
    
    if (result === 'ok') {
    resultMessage.textContent = 'Valid word!';
    const submittedWord = wordInput.value.toUpperCase();  // Get the submitted word again
    scoreDisplay.textContent = parseInt(scoreDisplay.textContent) + submittedWord.length;
    postStats(submittedWord.length);
    } else if (result === 'not-on-board') {
        resultMessage.textContent = 'Word is not on the board.';
    } else if (result === 'not-a-word') {
        resultMessage.textContent = 'Not a valid word.';
    }
}

startGameTimer();
