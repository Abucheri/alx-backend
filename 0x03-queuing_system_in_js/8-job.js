import kue from 'kue';

/**
 * Creates push notification jobs
 * @param {Array} jobs - Array of job objects
 * @param {Queue} queue - Kue queue instance
 */
const createPushNotificationsJobs = (jobs, queue) => {
  // Check if jobs is an array, if not, throw an error
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  // Loop through each job object in the jobs array
  jobs.forEach(jobData => {
    // Create a new job in the queue 'push_notification_code_3' with jobData
    const job = queue.create('push_notification_code_3', jobData)
      .save(err => {
        // If there's no error while saving the job, log the job ID
        if (!err) {
          console.log(`Notification job created: ${job.id}`);
        }
      });

    // Event listener for when the job is completed
    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });

    // Event listener for when the job fails
    job.on('failed', (err) => {
      console.log(`Notification job ${job.id} failed: ${err}`);
    });

    // Event listener for job progress updates
    job.on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  });
};

export default createPushNotificationsJobs;
