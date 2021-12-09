def run_with_retry(notebook, timeout, args = {}, max_retries = 3):
  num_retries = 0
  while True:
    try:
      return dbutils.notebook.run(notebook, timeout, args)
    except Exception as e:
      if num_retries > max_retries:
        raise e
      else:
        print("Retrying error", e)
        num_retries += 1
 ENVIRONMENT = dbutils.widgets.get('environment')
#  enviroment is the parameter of existing jobs
# to execute
run_with_retry("/Users/tony/prod/UpdateAllBMC", 25200,args = {'environment':ENVIRONMENT}, max_retries = 0)
