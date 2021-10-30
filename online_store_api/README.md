# Installation Guide
## Without Docker
1. Install Python3.8 or higher
2. Install PostgreSQL 12
3. Clone Repository
4. Create Virtual Environtment
	```bash
	python3.8 -m venv venv
	```
		
5. Activate Virtual Environtment
	```bash
	source venv/bin/activate
	```
6. Install Requirements
	```bash
	pip install -r requirements.txt
	```
7. Adjust value like database settings etc at file `.env`. Example value is put on `.env.example`. You can copy and modify it
    ```bash
    cp .env.example .env
    ```
8. Run Migrate
	```bash
	./manage.py migrate
	``` 
9. Run app
	```bash
	./manage.py runserver
	``` 
10. Open `localhost:8000/docs` to show api documentation

## With Dokcer
```bash
docker-compose up
```

## Demo
1. http://<demo-ip>:8000/swagger/


## Analysis
1. Describe what you think happened that caused those bad reviews during our 12.12 event and why it happened
    - Based on the cases described above. In my opinion, the causes of out stock are as follows:
        1. Lack of validation at checkout. The order bigger than available stock.
        2. Unhandled race condition. The application used sahared resources (product stock) at the same time. Concurrency problem.
2. Based on your analysis, propose a solution that will prevent the incidents from occurring again
    - My solution is:
        1. Lock the resource exclusively until one process order finished, to ensure only one thread can access/edit the resource.
            With mutex a way to ensure that only one thread is allowed inside that area, using that resource. In django has built-in method `select_for_update` to tell database to lock until transaction is completed.
