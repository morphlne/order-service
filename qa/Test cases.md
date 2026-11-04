# Scope of testing

Functional `/users` API testing (GET, POST, PUT, PATCH):

* Request schema validation
* Service logic follows the business rules
* Database data is modified according to requests

# Checklist

* Verify creation of user with valid name/email address
* Verify validation errors for invalid name/email on user creation
* Verify retrieval of all active users
* Verify retrieval of active user by id
* Verify error for inactive/nonexistent user by id
* Verify modification of a user's name/email with valid data
* Verify validation errors for invalid name/email on user modification
* Verify error on modification nonexistent/inactive user
* Verify deactivation of active user
* Verify error on activation of inactive user
* Verify error on activation/deactivation of nonexistent user

# Test Cases

### TC-USR-01: Create User

* **Precondition:** User with `email = alice.smith@example.com` doesn't persist in database
* **Method / Endpoint:** `POST /users`
* **Request Body:**
  ```json
  {
    "name": "Alice Smith",
    "email": "alice.smith@example.com"
  }
  ```
* **Expected Response:** `200 OK`
* **Database Verification:** A new row is added to the `users` table. The `user_id` is automatically assigned via
  identity, and `is_active` defaults to `true`.

### TC-USR-02: Create User with Invalid Name

* **Method / Endpoint:** `POST /users`
* **Request Body:**
  ```json
  {
    "name": "",
    "email": "alice.smith@example.com"
  }
  ```
* **Expected Response:** `422 Unprocessable Entity` (returns standard FastAPI validation structure
  `HTTPValidationError`)
* **Database Verification:** No changes in database

### TC-USR-03: Create User with Invalid Email

* **Method / Endpoint:** `POST /users`
* **Request Body:**
  ```json
  {
    "name": "Alice Smith",
    "email": "invalid-email-format"
  }
  ```
* **Expected Response:** `422 Unprocessable Entity` (returns standard FastAPI validation structure
  `HTTPValidationError`).
* **Database Verification:** No changes in database

### TC-USR-04: Create User with Duplicated Email

* **Precondition:** User with `email = alice.smith@example.com` persists in database
* **Method / Endpoint:** `POST /users`
* **Request Body:**
  ```json
  {
    "name": "Alice Junior",
    "email": "alice.smith@example.com"
  }
  ```
* **Expected Response:** `400 Bad Request`
* **Database Verification:** The service rejects the query due to the violation unique email business-rule

### TC-USR-05: Deactivate Active User

* **Precondition:** User with `user_id = 1` and `is_active = true` persists in database
* **Method / Endpoint:** `PATCH /users/{user_id}`
* **Path Parameter:** `user_id = 1`
* **Request Body:**
  ```json
  {
    "is_active": false
  }
  ```
* **Expected Response:** `200 OK`
* **Database Verification:** The `is_active` flag for the user with `user_id = 1` changes from `true` to `false`

### TC-USR-06: Deactivate Unknown User

* **Precondition:** User with `user_id = 999` doesn't persist in database
* **Method / Endpoint:** `PATCH /users/{user_id}`
* **Path Parameter:** `user_id = 999`
* **Request Body:**
  ```json
  {
    "is_active": false
  }
  ```
* **Expected Response:** `404 Not Found`
* **Database Verification:** No changes in database

### TC-USR-07: Activate Inactive User

* **Precondition:** User with `user_id = 1` and `is_active = false` persists in database
* **Method / Endpoint:** `PATCH /users/{user_id}`
* **Path Parameter:** `user_id = 1`
* **Request Body:**
  ```json
  {
    "is_active": true
  }
  ```
* **Expected Response:** `400 Bad Request`
* **Database Verification:** Keep `is_active = false` flag for the user with `user_id = 1`

### TC-USR-08: Activate Unknown User

* **Precondition:** User with `user_id = 999` doesn't persist in database
* **Method / Endpoint:** `PATCH /users/{user_id}`
* **Path Parameter:** `user_id = 999`
* **Request Body:**
  ```json
  {
    "is_active": true
  }
  ```
* **Expected Response:** `400 Bad Request`
* **Database Verification:** No changes in database

### TC-USR-09: Get All Active Users

* **Precondition:** Both `is_active = true / false` type of users persist in database
* **Method / Endpoint:** `GET /users`
* **Request Body:** None
* **Expected Response:** `200 OK` (returns a JSON array of all active users)
* **Database Verification:** The collection matches the count and field data found inside the `users` table with
  `is_active = true`

### TC-USR-10: Get Single Active User by ID

* **Precondition:** User with `user_id = 1` and `is_active = true` persists in database
* **Method / Endpoint:** `GET /users/{user_id}`
* **Path Parameter:** `user_id = 1`
* **Request Body:** None
* **Expected Response:** `200 OK`
* **Database Verification:** Returns data directly matching the row entity where `user_id = 1`

### TC-USR-11: Get Single Inactive User by ID

* **Precondition:** User with `user_id = 1` and `is_active = false` persists in database
* **Method / Endpoint:** `GET /users/{user_id}`
* **Path Parameter:** `user_id = 1`
* **Request Body:** None
* **Expected Response:** `404 Not Found`
* **Database Verification:** No changes in database

### TC-USR-12: Get Single User by Unknown ID

* **Precondition:** User with `user_id = 999` doesn't persist in database
* **Method / Endpoint:** `GET /users/{user_id}`
* **Path Parameter:** `user_id = 999`
* **Request Body:** None
* **Expected Response:** `404 Not Found`
* **Database Verification:** No changes in database

### TC-USR-13: Update Active User Information Profile

* **Precondition:** User with `user_id = 1` and `is_active = true` persists in database. No user has email
  `alice.peterson@example.com`
* **Method / Endpoint:** `PUT /users/{user_id}`
* **Path Parameter:** `user_id = 1`
* **Request Body:**
  ```json
  {
    "name": "Alice Peterson",
    "email": "alice.peterson@example.com"
  }
  ```
* **Expected Response:** `200 OK`
* **Database Verification:** Updates the corresponding row columns fields for the user with `user_id = 1`

### TC-USR-14: Update Active User Information Profile With Invalid Name

* **Precondition:** User with `user_id = 1` and `is_active = true` persists in database
* **Method / Endpoint:** `PUT /users/{user_id}`
* **Path Parameter:** `user_id = 1`
* **Request Body:**
  ```json
  {
    "name": "",
    "email": "alice.peterson@example.com"
  }
  ```
* **Expected Response:** `422 Unprocessable Entity` (returns standard FastAPI validation structure
  `HTTPValidationError`)
* **Database Verification:** No changes in database

### TC-USR-15: Update Active User Information Profile With Invalid Email

* **Precondition:** User with `user_id = 1` and `is_active = true` persists in database
* **Method / Endpoint:** `PUT /users/{user_id}`
* **Path Parameter:** `user_id = 1`
* **Request Body:**
  ```json
  {
    "name": "Alice Peterson",
    "email": "invalid-email-format"
  }
  ```
* **Expected Response:** `422 Unprocessable Entity` (returns standard FastAPI validation structure
  `HTTPValidationError`)
* **Database Verification:** No changes in database

### TC-USR-16: Update Active User Information Profile With Duplicated email

* **Precondition:** User with `user_id = 1` and `is_active = true` persists in database. User with `user_id = 2` has
  email `alice.peterson@example.com`
* **Method / Endpoint:** `PUT /users/{user_id}`
* **Path Parameter:** `user_id = 1`
* **Request Body:**
  ```json
  {
    "name": "Alice Peterson",
    "email": "alice.peterson@example.com"
  }
  ```
* **Expected Response:** `400 Bad Request`
* **Database Verification:** No changes in database

### TC-USR-17: Update Inactive User Information Profile

* **Precondition:** User with `user_id = 1` and `is_active = false` persists in database
* **Method / Endpoint:** `PUT /users/{user_id}`
* **Path Parameter:** `user_id = 1`
* **Request Body:**
  ```json
  {
    "name": "Alice Peterson",
    "email": "alice.peterson@example.com"
  }
  ```
* **Expected Response:** `404 Not Found`
* **Database Verification:** No changes in database

### TC-USR-18: Update Unknown User Information Profile

* **Precondition:** User with `user_id = 999` doesn't persist in database
* **Method / Endpoint:** `PUT /users/{user_id}`
* **Path Parameter:** `user_id = 999`
* **Request Body:**
  ```json
  {
    "name": "Alice Peterson",
    "email": "alice.peterson@example.com"
  }
  ```
* **Expected Response:** `404 Not Found`
* **Database Verification:** No changes in database
