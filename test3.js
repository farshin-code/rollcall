function testAPI(email,pass){

    fetch('http://127.0.0.1:5000/checkpassword',{
          method:'POST',
                                            body: formData
                                        })
                                            .then(response => response.json())
                                            .then(result => {
                                                //  r = ( 'true' == result['invalidUserPass'].toLowerCase())
                                                //  console.log(r)
                                                console.log('result is :',result)
                                            })
                                    .catch(error => {
                                                // handle any errors
                                                console.error(error);
                                            });
                                    
}