%% import data
delimiterIn = ' ';
s1 = importdata('r1.txt', delimiterIn);
s2 = importdata('r2.txt', delimiterIn);
s3 = importdata('r3.txt', delimiterIn);
s4 = importdata('r4.txt', delimiterIn);
s5 = importdata('r5.txt', delimiterIn);
s6 = importdata('r6.txt', delimiterIn);

%% plot 1
plot(s1);
hold on;
plot(s2);
plot(s3);

xlabel('trial');
ylabel('steps');

legend('1 agent', '2 agents', '3 agents');

%% plot 2
subplot(1,2,1);
plot(s3);
hold on;
plot(s4);
xlabel('trial');
ylabel('steps');
subplot(1,2,2);
plot(s3 - s4);
xlabel('trial');
ylabel('steps difference');
sum(s3-s4)


%% plot 3
plot(s5);
hold on;
plot(s6);