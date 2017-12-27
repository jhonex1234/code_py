 Properties props = new Properties();
		  props.setProperty("python.path","/home/jhonex/miniconda3/envs/nlp/bin/python");
		  props.setProperty("python.path","/home/jhonex/miniconda3/envs/nlp/bin/python3.5");
		  Runtime.exec("activate nlp");
		  PySystemState.initialize(System.getProperties(),props,null);
		
		  String val1="";
		  PythonInterpreter python = new PythonInterpreter();
		  
		  python.exec("import sys");
		  python.exec("sys.path.insert(0,r'/home/jhonex/miniconda3/envs/nlp/bin/python')");
		  python.exec("sys.path.insert(0,r'/home/jhonex/miniconda3/envs/nlp/bin/python3.5')");
			  
		  python.exec("sys.path.insert(0,r'/home/jhonex/workspace/java_json/src/com/python/')");
		  python.exec("import friend");
		  python.exec("d=friend.know('juan','28','codificar')");
	      val1 = python.get("d").toString();
	      System.out.print(val1);
