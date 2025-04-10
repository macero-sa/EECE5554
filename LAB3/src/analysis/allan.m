% MATLAB script to read a ROS1 .bag file, compute Allan variance, and extract parameters for VNYMR messages

% Add necessary paths
% addpath('/path/to/rosbag/matlab/functions'); % Adjust if necessary
% addpath('/path/to/your/allan_variance_functions'); % Allan variance calculation functions

% Load ROSbag file
bag = rosbag('LocationD.bag');  % Replace with your bag file path

% Select the VectorNav topic (you should change the topic name if needed)
vectornav_topic = '/vectornav'; % Adjust to match your topic name
vectornav_msgs = select(bag, 'Topic', vectornav_topic);

% Read VectorNav messages from the bag
vectornav_data = readMessages(vectornav_msgs, 'DataFormat', 'struct');
% accx8 accy9 accz10 gyrox11 gyroy12 gyroz13
time = [];
gyro_x = [];
gyro_y = [];
gyro_z = [];
accel_x = [];
accel_y = [];
accel_z = [];

for i = 1:length(vectornav_data)

    time = [time; vectornav_data{i}.Header.Stamp.Sec + vectornav_data{i}.Header.Stamp.Nsec * 1e-9];
    data_string = vectornav_data{i}.Data;
    data_values = str2double(strsplit(data_string, ','));
    rm_cehcksum = strsplit(data_string, '*'); 
    data_values = str2double(strsplit(rm_cehcksum{1}, ','));

    gyro_x = [gyro_x; data_values(11)];
    gyro_y = [gyro_y; data_values(12)];
    gyro_z = [gyro_z; data_values(13)];

    accel_x = [accel_x; data_values(8)];
    accel_y = [accel_y; data_values(9)];
    accel_z = [accel_z; data_values(10)];


end


%% 
% Plot the gyroscope data
% time = time(1:length(gyro_x));
% figure;
% subplot(3,1,1);
% plot(time, gyro_x);
% title('Gyroscope X-axis');
% xlabel('Time (s)');
% ylabel('Angular Velocity (rad/s)');
% 
% subplot(3,1,2);
% plot(time, gyro_y);
% title('Gyroscope Y-axis');
% xlabel('Time (s)');
% ylabel('Angular Velocity (rad/s)');
% 
% subplot(3,1,3);
% plot(time, gyro_z);
% title('Gyroscope Z-axis');
% xlabel('Time (s)');
% ylabel('Angular Velocity (rad/s)');

% Sampling rate (or dt, adjust based on your IMU frequency)
dt = mean(diff(time));  % Time step between consecutive data points
L = size(gyro_x,1)
maxM = 2.^floor(log2(L/2));
fs = 1 / dt; % Sampling frequency (Hz)
m = logspace(log10(1), log10(maxM), 100); 
m = round(m); % Round to nearest integer
m = unique(m); 

% Compute Allan Variance for gyro x, y, z
[avar_gx, tau_gx] = allanvar(gyro_x, m, fs);
[avar_gy, tau_gy] = allanvar(gyro_y, m, fs);
[avar_gz, tau_gz] = allanvar(gyro_z, m, fs);

[avar_ax, tau_ax] = allanvar(accel_x, m, fs);
[avar_ay, tau_ay] = allanvar(accel_y, m, fs);
[avar_az, tau_az] = allanvar(accel_z, m, fs);

adev_gx = sqrt(avar_gx);
adev_gy = sqrt(avar_gy);
adev_gz = sqrt(avar_gz);
adev_ax = sqrt(avar_ax);
adev_ay = sqrt(avar_ay);
adev_az = sqrt(avar_az);

% N
slope = -0.5;
logtau_gx = log10(tau_gx);
logadev_gx = log10(adev_gx);
dlogadev_gx = diff(logadev_gx) ./ diff(logtau_gx);
[~, i] = min(abs(dlogadev_gx - slope));

% Find the y-intercept of the line.
b_gx = logadev_gx(i) - slope*logtau_gx(i);

% Determine the angle random walk coefficient from the line.
logN_gx = slope*log(1) + b_gx;
N_gx = 10^logN_gx

tauN_gx = 1;
lineN_gx = N_gx ./ sqrt(tau_gx);


% K
slope = 0.5;
logtau_gx = log10(tau_gx);
logadev_gx = log10(adev_gx);
dlogadev_gx = diff(logadev_gx) ./ diff(logtau_gx);
[~, i] = min(abs(dlogadev_gx - slope));

% Find the y-intercept of the line.
b_gx = logadev_gx(i) - slope*logtau_gx(i);

% Determine the rate random walk coefficient from the line.
logK_gx = slope*log10(3) + b_gx;
K_gx = 10^logK_gx

tauK_gx = 3;
lineK_gx = K_gx .* sqrt(tau_gx/3);

% B
slope = 0;
logtau_gx = log10(tau_gx);
logadev_gx = log10(adev_gx);
dlogadev_gx = diff(logadev_gx) ./ diff(logtau_gx);
[~, i] = min(abs(dlogadev_gx - slope));

% Find the y-intercept of the line.
b_gx = logadev_gx(i) - slope*logtau_gx(i);

% Determine the bias instability coefficient from the line.
scfB_gx = sqrt(2*log(2)/pi);
logB_gx = b_gx - log10(scfB_gx);
B_gx = 10^logB_gx

tauB_gx = tau_gx(i);
lineB_gx = B_gx * scfB_gx * ones(size(tau_gx));

% plot
tauParams_gx = [tauN_gx, tauK_gx, tauB_gx];
params_gx = [N_gx, K_gx, scfB_gx*B_gx];
figure
loglog(tau_gx, adev_gx, tau_gx, [lineN_gx, lineK_gx, lineB_gx], '--', ...
    tauParams_gx, params_gx, 'o')
title('Allan Deviation with Noise Parameters Gyro_x')
xlabel('\tau')
ylabel('\sigma(\tau)')
legend('$\sigma (rad/s)$', '$\sigma_N ((rad/s)/\sqrt{Hz})$', ...
    '$\sigma_K ((rad/s)\sqrt{Hz})$', '$\sigma_B (rad/s)$', 'Interpreter', 'latex')
text(tauParams_gx, params_gx, {'N', 'K', '0.664B'})
grid on
axis equal

%%
% Function to compute noise parameters (N, K, B) for a given gyro axis
function [N, K, B, tauN, tauK, tauB, lineN, lineK, lineB] = compute_allan_params(tau, adev, axis_label)
    % Angle Random Walk (N)
    slope = -0.5;
    logtau = log10(tau);
    logadev = log10(adev);
    dlogadev = diff(logadev) ./ diff(logtau);
    [~, i] = min(abs(dlogadev - slope));
    b = logadev(i) - slope * logtau(i);
    logN = slope * log10(1) + b;
    N = 10^logN;
    tauN = 1;
    lineN = N ./ sqrt(tau);

    % Rate Random Walk (K)
    slope = 0.5;
    [~, i] = min(abs(dlogadev - slope));
    b = logadev(i) - slope * logtau(i);
    logK = slope * log10(3) + b;
    K = 10^logK;
    tauK = 3;
    lineK = K .* sqrt(tau / 3);

    % Bias Instability (B)
    slope = 0;
    [~, i] = min(abs(dlogadev - slope));
    b = logadev(i) - slope * logtau(i);
    scfB = sqrt(2 * log(2) / pi);
    logB = b - log10(scfB);
    B = 10^logB;
    tauB = tau(i);
    lineB = B * scfB * ones(size(tau));

    % Plot results
    tauParams = [tauN, tauK, tauB];
    params = [N, K, scfB * B];

    figure;
    loglog(tau, adev, tau, [lineN, lineK, lineB], '--', tauParams, params, 'o');
    title(['Allan Deviation with Noise Parameters ', axis_label]);
    xlabel('\tau');
    ylabel('\sigma(\tau)');
    legend('$\sigma (rad/s)$', '$\sigma_N ((rad/s)/\sqrt{Hz})$', ...
        '$\sigma_K ((rad/s)\sqrt{Hz})$', '$\sigma_B (rad/s)$', 'Interpreter', 'latex');
    text(tauParams, params, {'N', 'K', '0.664B'});
    grid on;
    axis equal;
end

% Compute noise parameters for gyro_x, gyro_y, and gyro_z
[N_gx, K_gx, B_gx, tauN_gx, tauK_gx, tauB_gx, lineN_gx, lineK_gx, lineB_gx] = compute_allan_params(tau_gx, adev_gx, 'Gyro_x');
[N_gy, K_gy, B_gy, tauN_gy, tauK_gy, tauB_gy, lineN_gy, lineK_gy, lineB_gy] = compute_allan_params(tau_gy, adev_gy, 'Gyro_y');
[N_gz, K_gz, B_gz, tauN_gz, tauK_gz, tauB_gz, lineN_gz, lineK_gz, lineB_gz] = compute_allan_params(tau_gz, adev_gz, 'Gyro_z');

[N_ax, K_ax, B_ax, tauN_ax, tauK_ax, tauB_ax, lineN_ax, lineK_ax, lineB_ax] = compute_allan_params(tau_ax, adev_ax, 'Accel_x');
[N_ay, K_ay, B_ay, tauN_ay, tauK_ay, tauB_ay, lineN_ay, lineK_ay, lineB_ay] = compute_allan_params(tau_ay, adev_ay, 'Accel_y');
[N_az, K_az, B_az, tauN_az, tauK_az, tauB_az, lineN_az, lineK_az, lineB_az] = compute_allan_params(tau_az, adev_az, 'Accel_z');

