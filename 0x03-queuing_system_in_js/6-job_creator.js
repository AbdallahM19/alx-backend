import { createQueue } from 'kue';

const queueKue = createQueue();

const jobData = {
  phoneNumber: '1234567890',
  message: 'This is a test message',
};

const job = queueKue.create('push_notification_code', jobData)
  .save((err) => {
    if (!err) {
      console.log(`Notification job created: ${job.id}`);
    }
  });

job.on('complete', () => {
  console.log('Notification job completed');
}).on('failed', () => {
  console.log('Notification job failed');
});
