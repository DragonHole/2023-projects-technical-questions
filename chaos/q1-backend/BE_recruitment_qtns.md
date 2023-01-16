1.  Identify one problem in the below code block, will this code compile? Discuss the related Rust feature regarding the problem you have identified, why does Rust choose to include this feature? A few sentences are good enough.

    ```rust
        let data = vec![1, 2, 3];
        let my_ref_cell = RefCell::new(69);
        let ref_to_ref_cell = &my_ref_cell;

        std::thread::spawn(move || {

            println!("captured {data:?} by value");

            println!("Whats in the cell?? {ref_to_ref_cell:?}")

        }).join().unwrap();
    ```

    A: Refcell allows data mutation when there are existing immutable references to that data, Refcell basically turns the compiler statically checked borrow rules into rules checked at runtime. There is no thread synchronization performed, so multi-thread access will lead to data race. But since it doesn't implement the Sync trait, it doesn't even pass the compiler check for being passed into the `std::thread::spawn()` function. 

2.  Shortly discuss, when modelling a response to a HTTP request in Rust, would you prefer to use `Option` or `Result`?

    A: `Option` can contain either `Some` and contains a value or `None`. In the case of HTTP response, we can't just return a response modelled with `None`, but instead we need to represent multiple possible error states(404, 500, or etc). This can be achieved with `Result`, as it represents `Ok`(200) or `Err`(some error code). 

3.  In `student.psv` there are some fake student datas from UNSW CSE (no doxx!). In each row, the fields from left to right are

    - UNSW Course Code
    - UNSW Student Number
    - Name
    - UNSW Program
    - UNSW Plan
    - WAM
    - UNSW Session
    - Birthdate
    - Sex

    Write a Rust program to find the course which has the highest average student WAM. **Write your program in the cargo project q3**.

