// handle adding listing to user's database
const dbListingForm = document.querySelectorAll('.db_listing_form')
const yelpListingForm = document.querySelectorAll('.yelp_listing_form')


for (const form of dbListingForm) {
    form.addEventListener('submit', (evt) =>{
        const submiiterId = form.querySelector('[name="submitter"]').value;
        if (submiiterId == user_id) {
            evt.preventDefault();
            alert("It can't be added, that's your own listing!")
        }
        else if(user_id === null) {
            evt.preventDefault();
            alert("Please log in!")
        }
        
    })}

for (const form of yelpListingForm) {
    form.addEventListener('submit', (evt) =>{
        
        if(user_id === null) {
            evt.preventDefault();
            alert("Please log in!")
        }
            
        })}


// set certain listing in user's database as one of the favorite listings
favoriteButtons = document.querySelectorAll('.favorite_button');

for (const button of favoriteButtons) {
    button.addEventListener('click', (evt) => {
        // evt.preventDefault();
        const formInputs = {
        listing_id : button.id
        }
        const url = '/user_listings/favorite.json'
        const params = {
            method:'POST',
            body: JSON.stringify(formInputs),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        fetch(url,params)
            .then ((response) => response.json())
            .then((responseJson) =>{
                document.querySelector('#favorite_listing').innerHTML = responseJson.msg
            })
    })
}

// add deleting feature to user's listing page 
deleteButtons = document.querySelectorAll('.delete_listing_button');

for (const button of deleteButtons) {
    button.addEventListener('click', (evt) => {
        evt.preventDefault();
        const formInputs = {
        listing_id : button.id
        }
        const url = '/user_listings/delete'
        const params = {
            method:'POST',
            body: JSON.stringify(formInputs),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        fetch(url,params)
            .then ((response) => {
                if (response.redirected) {
                    window.location.href = response.url;
                }
            })
            
    })
}

