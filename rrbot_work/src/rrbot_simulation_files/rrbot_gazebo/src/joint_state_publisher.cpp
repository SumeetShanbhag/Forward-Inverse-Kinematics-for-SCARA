#include "custom_interfaces/srv/find_joint_states.hpp"
#include "rclcpp/rclcpp.hpp"
#include <bits/stdc++.h>
#include <math.h>
#include <memory>

void add(const std::shared_ptr<custom_interfaces::srv::FindJointStates::Request> request, std::shared_ptr<custom_interfaces::srv::FindJointStates::Response> response)
{
    std::double_t x = round(request->x * 100) / 100; // x component of the end effector pose
    std::double_t y = round(request->y * 100) / 100; // y component of the end effector pose
    std::double_t z = round(request->z * 100) / 100; // z component of the end effector pose

    std::double_t d, cq2, q2, cq1, q1;

    d = z - 1.2;
    cq2 = (x*x + y*y - 2.05 * 2.05 - 0.81) / (2 * 2.05 * 0.9);
    q2 = acos(cq2);
//    cq1 = (x * (2.05 + 0.9 * cq1)) - y*sqrt((x*x + y*y - (2.05 + 0.9 * cq2))) / (x*x + y*y);
//    q1 = acos(cq1);
    q1 = atan2(y,x) - atan2(0.9*sin(q2), (2.05 + 0.9*cos(q2)));
    
    response->q1 = q1;
    response->q2 = q2;
    response->q3 = d;
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "(x,y,z): ('%f','%f','%f')", request->x, request->y, request->z);
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "(q1,q2,q3): ('%f','%f','%f')", response->q1, response->q2, response->q3);
}

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("ikin");
    rclcpp::Service<custom_interfaces::srv::FindJointStates>::SharedPtr service = node->create_service<custom_interfaces::srv::FindJointStates>("ikin_ser", &add);
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Calculating Ikin.");
    rclcpp::spin(node);
    rclcpp::shutdown();
}