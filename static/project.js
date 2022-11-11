// dbListingButtons = document.querySelectorAll('.db_listing_button')
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