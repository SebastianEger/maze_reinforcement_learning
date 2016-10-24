%%
delimiterIn = ' ';
coop_abs = importdata('coop_abs.txt', delimiterIn);
plot(coop_abs);
hold on;
xlabel('trial');
ylabel('steps');

%% load data
delimiterIn = ' ';
a1_exp = importdata('data_agent0_expertness.txt', delimiterIn);
a2_exp = importdata('data_agent1_expertness.txt', delimiterIn);
a3_exp = importdata('data_agent2_expertness.txt', delimiterIn);

a1_steps = importdata('data_agent0_steps.txt', delimiterIn);
a2_steps = importdata('data_agent1_steps.txt', delimiterIn);
a3_steps = importdata('data_agent2_steps.txt', delimiterIn);

steps = importdata('data.txt', delimiterIn);

%% plot steps
plot(a1_steps);
hold on;
plot(a2_steps);
plot(a3_steps);

%% if expertness is distance to goal
plot(a1_exp(1:steps(1)));
hold on;
plot(a2_exp(1:steps(1)));
hold on;
plot(a3_exp(1:steps(1)));

%% if expertness is normal


%%
subplot(1,3,1);
plot(a1_exp);
subplot(1,3,2);
plot(a2_exp);
subplot(1,3,3);
plot(a3_exp);