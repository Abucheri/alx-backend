import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';

const queue = kue.createQueue(); // Creating a Kue queue instance

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
];

// Test suite for createPushNotificationsJobs function
describe('createPushNotificationsJobs', () => {
  // Setting up test mode before running tests
  before(() => {
    queue.testMode.enter();
  });

  // Cleaning up after each test
  afterEach(() => {
    queue.testMode.clear();
  });

  // Exiting test mode after all tests are done
  after(() => {
    queue.testMode.exit();
  });

  // Test case: Display an error message if jobs is not an array passing Number
  it('display a error message if jobs is not an array passing Number', () => {
    expect(() => {
      createPushNotificationsJobs(2, queue);
    }).to.throw('Jobs is not an array');
  });

  // Test case: Display an error message if jobs is not an array passing Object
  it('display a error message if jobs is not an array passing Object', () => {
    expect(() => {
      createPushNotificationsJobs({}, queue);
    }).to.throw('Jobs is not an array');
  });

  // Test case: Display an error message if jobs is not an array passing String
  it('display a error message if jobs is not an array passing String', () => {
    expect(() => {
      createPushNotificationsJobs('Hello', queue);
    }).to.throw('Jobs is not an array');
  });

  // Test case: Should NOT display an error message if jobs is an array with empty array
  it('should NOT display a error message if jobs is an array with empty array', () => {
    const ret = createPushNotificationsJobs([], queue);
    expect(ret).to.equal(undefined);
  });

  // Test case: Create two new jobs to the queue
  it('create two new jobs to the queue', () => {
    // Creating two jobs
    queue.createJob('myJob', { foo: 'bar' }).save();
    queue.createJob('anotherJob', { baz: 'bip' }).save();

    // Assertions for the created jobs
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('myJob');
    expect(queue.testMode.jobs[0].data).to.eql({ foo: 'bar' });
    expect(queue.testMode.jobs[1].type).to.equal('anotherJob');
    expect(queue.testMode.jobs[1].data).to.eql({ baz: 'bip' });
  });
});
