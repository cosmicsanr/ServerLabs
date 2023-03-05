import {
    installValidators,
    validateAllFields,
    resetAllFields,
    addPredicates,
} from './validations.js';

import {
    bySel,
    whenClick,
    syncWait,
    isValidDate,
    byPOSTasJSON,
} from './utils.js';


const URL = 'http://127.0.0.1:8000';


addPredicates({
    'date_DD/MM/YYYY': isValidDate,
    tournamentName: /([A-Za-z]+)\s?/,
});

window.addEventListener('load', function () {
    installValidators();
    whenClick('reset', e => resetAllFields());
    whenClick('submit', validateAndSubmitFormTournament);
});


async function registerTournament() {
    const tournament = {
        name: bySel('[name=tournamentName]').value,
        start_date: bySel('[name=startDate]').value,
        end_date: bySel('[name=endDate]').value,

    };
    const response = await byPOSTasJSON(`${URL}/tournaments`, tournament);
    return [response.ok, await response.json()];
}

async function validateAndSubmitFormTournament() {
    if (!validateAllFields()) {
        return;
    }
    try {
        const [responseOK, responseData] = await registerTournament();
        const showStatusFn = responseOK ? showSuccess : showError;
        showStatusFn(responseData);
    }
    catch (error) {
        console.error(`ERROR: An error has ocurred when connecting to server at ${URL}`)
        console.error(error);
    }
}

/**
 * @param {Object} responseData 
 */
function showSuccess(responseData) {
    const msg = `Torneio inserido com sucesso.<br>
Torneio: ${responseData.name} <br>
ID: ${responseData.id}`;
    const formFields = document.querySelector('.info');
    formFields.style.display = 'none';
    const elemsToHide = document.querySelectorAll('form > button, .checkbox');
    elemsToHide.forEach(elem => elem.style.display = 'none');
    showSubmissionInfo(msg, true);
}

/**
 * @param {Object} responseData 
 */
function showError(responseData) {
    const errorInfo = responseData.detail;
    const msg = `Não foi possível inserir torneio. ${errorInfo.error_msg}`;
    showSubmissionInfo(msg, false);
}

function showSubmissionInfo(msg, success) {
    const submissionStatusElem = document.querySelector('.submission-status');
    const [cssClassToAdd, cssClassToRem] = (success ?
        ['submission-status-ok', 'submission-status-error']
        : ['submission-status-error', 'submission-status-ok']
    );
    submissionStatusElem.innerHTML = `${msg}`;
    submissionStatusElem.classList.add(cssClassToAdd);
    submissionStatusElem.classList.remove(cssClassToRem);
}


