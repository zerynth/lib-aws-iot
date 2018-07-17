.. module:: aws_iot_jobs

************************************
Amazon Web Services IoT Jobs Library
************************************

The Zerynth AWS IoT Jobs Library can be used to handle `IoT Jobs <https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html>`_ with ease.

    
==========
Jobs class
==========

.. class:: Jobs(thing)

    This class allows the retrieval of the :samp:`thing` job list.
    
    It requires the connection to thw MQTT broker to be already established: It subscribes to various
    topic to receive jobs notifications.

    
.. method:: changed()

    Return True if there are new pending jobs. If called again, and in the meantime no new job notifications have been received, return False.

    
.. method:: list()

    Retrieve the list of jobs for the current Thing. The result value is a tuple with two items. The first item is the list of IN_PROGRESS jobs, while the second item is the list of QUEUED jobs (as :class:`Job` instances). 

    This method is *blocking*. Control is not released until the list of jobs is retrieved. Moreover, it is not safe to call the method from different threads.

    
=========
Job class
=========

.. class:: Job(thing,jobid)

    This class abstracts an IoT Job related to a particular :samp:`thing` and having jobId :samp:`jobid`.
    There is no need to manually create instances of this class, they are returned by methods of the :class:`Jobs` class.

    
.. method:: describe()

    Retrieves data about the job. In particular the fields :samp:`version`, :samp:`status` and :samp:`document` are associated to the job instance after a successful :samp:`describe`.
    
    This method is *blocking*. Control is not released until the job description is retrieved. Moreover, it is not safe to call the method from different threads.

    Return True on success, False otherwise.

    
.. method:: update(status,status_details={})

    Updates the status of the job. The :samp:`status` can be one of the following class constant:

    * :samp:`Job.IN_PROGRESS`
    * :samp:`Job.FAILED`
    * :samp:`Job.SUCCEEDED`

    The optional field :samp:`status_details` can contain custom values that are associated to the job status.

    This method is *blocking*. Control is not released until the status change is signaled. Moreover, it is not safe to call the method from different threads.

    Return True on success, False otherwise.

    
