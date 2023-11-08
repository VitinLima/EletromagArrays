# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 17:48:55 2023

@author: Vítor Lima Aguirra
"""

import pickle
import time

import numpy as np
import csv
from scipy.interpolate import RegularGridInterpolator

from NumpyExpressionParser import NumpyExpressionParser as NEP
import MyMath
import AntennaEditorFrame

constants = dict()
constants["c"] = 299792458  # m/s
constants["f"] = 433e6  # Hz
constants["eta"] = 120 * np.pi
constants["lam"] = constants["c"] / constants["f"]  # m
constants["w"] = 2 * np.pi * constants["f"]  # rad/s
constants["k"] = 2 * np.pi / constants["lam"]  # rad/m


class Antenna:
    EditorFrame = AntennaEditorFrame.AntennaEditorFrame

    def __init__(
        self,
        constants=None,
        name="new antenna",
        current_magnitude=1,
        current_phase=0,
        theta=np.linspace(0, 180, 21),
        phi=np.linspace(-180, 180, 21),
        local_theta_deg=np.linspace(0, 180, 91),
        local_phi_deg=np.linspace(-180, 180, 91),
        elevation=0,
        azimuth=0,
        roll=0,
        x=0,
        y=0,
        z=0,
        evaluate_as="ideal dipole",
    ):
        # self.constants=constants
        self.name = name
        self.current_magnitude = current_magnitude
        self.current_phase = current_phase
        self.theta = theta
        self.phi = phi
        self.local_theta_deg = local_theta_deg
        self.local_phi_deg = local_phi_deg
        self.elevation = elevation
        self.azimuth = azimuth
        self.roll = roll
        self.x = x
        self.y = y
        self.z = z
        self.evaluate_as = evaluate_as

        self.mesh_phi, self.mesh_theta = np.meshgrid(
            np.radians(self.phi), np.radians(self.theta)
        )
        self.sin_mesh_phi = np.sin(self.mesh_phi)
        self.sin_mesh_theta = np.sin(self.mesh_theta)
        self.shape = (self.theta.size, self.phi.size)

        self.F = np.zeros(self.shape)
        self.Fphi = np.zeros(self.shape, dtype=np.csingle)
        self.Ftheta = np.zeros(self.shape, dtype=np.csingle)
        self.Frhcp = np.zeros(self.shape, dtype=np.csingle)
        self.Flhcp = np.zeros(self.shape, dtype=np.csingle)
        self.Fx = np.zeros(self.shape, dtype=np.csingle)
        self.Fy = np.zeros(self.shape, dtype=np.csingle)
        self.Fz = np.zeros(self.shape, dtype=np.csingle)
        self.Fref = np.zeros(self.shape, dtype=np.csingle)
        self.Fcross = np.zeros(self.shape, dtype=np.csingle)

        self.listeners = []
        self.antenna_size = 0.5
        self.silent = False
        self.local_mesh_N_theta = 91
        self.local_mesh_N_phi = 91

        self.evaluation_time = 0

        self.local_theta = np.radians(self.local_theta_deg)
        self.local_phi = np.radians(self.local_phi_deg)
        self.local_theta_rad = self.local_theta
        self.local_phi_rad = self.local_phi

        self.evaluation_arguments = dict()
        self.evaluation_arguments["dipole length"] = 0.5
        self.evaluation_arguments["loop dipole area"] = 0.5
        self.evaluation_arguments["expression theta"] = (
            "(cos(k*L*lam/2*cos(theta)) - "
            + "cos(k*L*lam/2))/(sin(theta)+(sin(theta)==0))"
        )
        self.evaluation_arguments["expression phi"] = "S*k*sin(theta)"
        self.evaluation_arguments["isotropic on"] = "theta"
        self.evaluation_arguments["file path"] = ""
        self.evaluation_arguments["force reload"] = False
        self.evaluation_arguments["load mesh from file"] = False

        self.evaluate_local_mesh()
        self.evaluate_R()
        self.evaluate_Rtheta()
        self.evaluate_Rphi()
        self.evaluate_hats()

        self.local_mesh_flag = False
        self.R_flag = False
        self.Relevation_flag = True
        self.Razimuth_flag = True
        self.Rtheta_flag = False
        self.Rphi_flag = False
        self.hats_flag = False
        self.LG_interp_mesh_flag = True
        self.local_field_flag = True
        self.ok = False

    def notify(self, caller, event):
        self.ok = False
        self.mark_update(
            '"'
            + str(caller)
            + '" called notify with event "'
            + event
            + '"'
        )

    def mark_update(self, event):
        if self.silent:
            return
        for l in self.listeners:
            l.notify(self, event)

    def set_name(self, name):
        self.name = name
        self.mark_update("renamed")

    def set_evaluation_method(self, evaluation_method):
        self.evaluate_as = evaluation_method
        self.local_field_flag = True
        self.ok = False

    def set_orientation(
        self, roll=None, azimuth=None, elevation=None
    ):
        if roll is not None:
            self.roll = roll
        if azimuth is not None:
            self.azimuth = azimuth
        if elevation is not None:
            self.elevation = elevation

        self.R_flag = True
        self.LG_interp_mesh_flag = True
        self.ok = False

    def set_position(self, x=None, y=None, z=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z

    def set_current(self, magnitude=None, phase=None):
        if magnitude is not None:
            self.current_magnitude = magnitude
        if phase is not None:
            self.current_phase = phase

        self.ok = False

    def resample(self, theta, phi):
        self.phi = phi
        self.theta = theta
        self.mesh_phi, self.mesh_theta = np.meshgrid(
            np.radians(self.phi), np.radians(self.theta)
        )
        self.shape = (self.theta.size, self.phi.size)
        self.F = np.zeros(self.shape)
        self.Fphi = np.zeros(self.shape, dtype=np.csingle)
        self.Ftheta = np.zeros(self.shape, dtype=np.csingle)
        self.Frhcp = np.zeros(self.shape, dtype=np.csingle)
        self.Flhcp = np.zeros(self.shape, dtype=np.csingle)
        self.Fx = np.zeros(self.shape, dtype=np.csingle)
        self.Fy = np.zeros(self.shape, dtype=np.csingle)
        self.Fz = np.zeros(self.shape, dtype=np.csingle)
        self.Fref = np.zeros(self.shape, dtype=np.csingle)
        self.Fcross = np.zeros(self.shape, dtype=np.csingle)

        self.Relevation_flag = True
        self.Razimuth_flag = True
        self.Rtheta_flag = True
        self.Rphi_flag = True
        self.hats_flag = True
        self.LG_interp_mesh_flag = True
        self.ok = False

    def evaluate_local_mesh(self):
        self.local_mesh_flag = False

        self.local_mesh_phi, self.local_mesh_theta = np.meshgrid(
            self.local_phi, self.local_theta
        )
        self.local_shape = (
            self.local_theta.size,
            self.local_phi.size,
        )
        self.local_mesh_theta_rad = self.local_mesh_theta
        self.local_mesh_phi_rad = self.local_mesh_phi
        self.sin_local_mesh_phi = np.sin(self.local_mesh_phi_rad)
        self.sin_local_mesh_theta = np.sin(self.local_mesh_theta_rad)

        self.local_hat_k = np.zeros(
            (self.local_theta.size, self.local_phi.size, 3)
        )
        self.local_hat_theta = np.zeros_like(self.local_hat_k)
        self.local_hat_phi = np.zeros_like(self.local_hat_k)
        self.local_hat_k[:, :, 2] = 1
        self.local_hat_theta[:, :, 0] = 1
        self.local_hat_phi[:, :, 1] = 1

        Rtheta = MyMath.roty(self.local_mesh_theta_rad)
        Rphi = MyMath.rotz(self.local_mesh_phi_rad)
        R = np.matmul(Rphi, Rtheta)
        self.local_hat_k = np.matmul(
            R, self.local_hat_k[:, :, :, np.newaxis]
        ).squeeze()
        self.local_hat_theta = np.matmul(
            R, self.local_hat_theta[:, :, :, np.newaxis]
        ).squeeze()
        self.local_hat_phi = np.matmul(
            R, self.local_hat_phi[:, :, :, np.newaxis]
        ).squeeze()

    def evaluate_R(self):
        self.R_flag = False

        cp = np.cos(np.radians(self.azimuth))
        sp = np.sin(np.radians(self.azimuth))
        Rbeta = np.zeros((3, 3))
        Rbeta[0, 0] = cp
        Rbeta[0, 1] = sp
        Rbeta[1, 0] = -sp
        Rbeta[1, 1] = cp
        Rbeta[2, 2] = 1
        ct = np.cos(np.radians(self.elevation))
        st = np.sin(np.radians(self.elevation))
        Ralpha = np.zeros((3, 3))
        Ralpha[0, 0] = ct
        Ralpha[0, 2] = -st
        Ralpha[2, 0] = st
        Ralpha[1, 1] = 1
        Ralpha[2, 2] = ct
        cr = np.cos(np.radians(self.roll))
        sr = np.sin(np.radians(self.roll))
        Rroll = np.zeros((3, 3))
        Rroll[0, 0] = 1
        Rroll[1, 1] = cr
        Rroll[1, 2] = sr
        Rroll[2, 1] = -sr
        Rroll[2, 2] = cr
        self.R = np.zeros((1, 1, 3, 3))
        self.R[0, 0, :, :] = Rroll @ Ralpha @ Rbeta

    def evaluate_Rtheta(self):
        self.Rtheta_flag = False

        ct = np.cos(self.mesh_theta)
        st = np.sin(self.mesh_theta)
        self.Rtheta = np.zeros((self.theta.size, self.phi.size, 3, 3))
        self.Rtheta[:, :, 0, 0] = ct
        self.Rtheta[:, :, 0, 2] = st
        self.Rtheta[:, :, 2, 0] = -st
        self.Rtheta[:, :, 1, 1] = 1
        self.Rtheta[:, :, 2, 2] = ct

    def evaluate_Rphi(self):
        self.Rphi_flag = False

        cp = np.cos(self.mesh_phi)
        sp = np.sin(self.mesh_phi)
        self.Rphi = np.zeros((self.theta.size, self.phi.size, 3, 3))
        self.Rphi[:, :, 0, 0] = cp
        self.Rphi[:, :, 0, 1] = -sp
        self.Rphi[:, :, 1, 0] = sp
        self.Rphi[:, :, 1, 1] = cp
        self.Rphi[:, :, 2, 2] = 1

    def evaluate_hats(self):
        self.hats_flag = False

        self.hat_k = np.zeros((self.theta.size, self.phi.size, 3))
        self.hat_theta = np.zeros((self.theta.size, self.phi.size, 3))
        self.hat_phi = np.zeros((self.theta.size, self.phi.size, 3))
        self.hat_k[:, :, 2] = 1
        self.hat_theta[:, :, 0] = 1
        self.hat_phi[:, :, 1] = 1

        self.hat_k = MyMath.rotate(self.hat_k, self.Rtheta)
        self.hat_theta = MyMath.rotate(self.hat_theta, self.Rtheta)

        self.hat_k = MyMath.rotate(self.hat_k, self.Rphi)
        self.hat_theta = MyMath.rotate(self.hat_theta, self.Rphi)
        self.hat_phi = MyMath.rotate(self.hat_phi, self.Rphi)

    def evaluate_LG_interp_mesh(self):
        # L - Local
        # G - Global
        # GL - Global on Local for vectors or
        #   Global to Local for matrices
        # LG - Local on Global for vectors or
        #   Local to Global for matrices

        self.LG_interp_mesh_flag = False

        GL_hat_k = MyMath.rotate(self.hat_k, self.R)
        GL_hat_theta = MyMath.rotate(self.hat_theta, self.R)

        GL_x = GL_hat_k[:, :, 0]
        GL_y = GL_hat_k[:, :, 1]
        GL_z = GL_hat_k[:, :, 2]

        self.GL_interp_mesh_theta = np.arctan2(
            np.sqrt(GL_y * GL_y + GL_x * GL_x), GL_z
        )

        ids = (self.GL_interp_mesh_theta > 3) + (
            self.GL_interp_mesh_theta < 0.1
        )

        GL_x[ids] = GL_hat_theta[ids, 0]
        GL_y[ids] = GL_hat_theta[ids, 1]
        self.GL_interp_mesh_phi = np.arctan2(GL_y, GL_x)

        ct = np.cos(self.GL_interp_mesh_theta)
        st = np.sin(self.GL_interp_mesh_theta)
        Rtheta = np.zeros_like(self.Rtheta)
        Rtheta[:, :, 0, 0] = ct
        Rtheta[:, :, 0, 2] = st
        Rtheta[:, :, 2, 0] = -st
        Rtheta[:, :, 1, 1] = 1
        Rtheta[:, :, 2, 2] = ct

        cp = np.cos(self.GL_interp_mesh_phi)
        sp = np.sin(self.GL_interp_mesh_phi)
        Rphi = np.zeros_like(self.Rphi)
        Rphi[:, :, 0, 0] = cp
        Rphi[:, :, 0, 1] = -sp
        Rphi[:, :, 1, 0] = sp
        Rphi[:, :, 1, 1] = cp
        Rphi[:, :, 2, 2] = 1

        L_interp_hat_theta = np.zeros(
            (self.theta.size, self.phi.size, 3)
        )
        L_interp_hat_phi = np.zeros_like(L_interp_hat_theta)
        L_interp_hat_theta[:, :, 0] = 1
        L_interp_hat_phi[:, :, 1] = 1

        LG_R = np.swapaxes(self.R, 2, 3)
        self.LG_interp_hat_theta = MyMath.rotate(
            MyMath.rotate(
                MyMath.rotate(L_interp_hat_theta, Rtheta), Rphi
            ),
            LG_R,
        )
        self.LG_interp_hat_phi = MyMath.rotate(
            MyMath.rotate(
                MyMath.rotate(L_interp_hat_phi, Rtheta), Rphi
            ),
            LG_R,
        )

    def get_reference_polarization(self):
        sp = np.sin(self.mesh_phi)
        cp = np.cos(self.mesh_phi)
        st = np.sin(self.mesh_theta)
        ct = np.cos(self.mesh_theta)
        hat_i_ref_x = -(1 - ct) * sp * cp
        hat_i_ref_y = 1 - sp * sp * (1 - ct)
        hat_i_ref_z = -st * sp
        hat_i_ref = (
            np.array([hat_i_ref_x, hat_i_ref_y, hat_i_ref_z])
            .swapaxes(0, 1)
            .swapaxes(1, 2)
        )

        hat_i_cross_x = 1 - cp * cp * (1 - ct)
        hat_i_cross_y = -(1 - ct) * sp * cp
        hat_i_cross_z = -st * cp
        hat_i_cross = (
            np.array([hat_i_cross_x, hat_i_cross_y, hat_i_cross_z])
            .swapaxes(0, 1)
            .swapaxes(1, 2)
        )

        return hat_i_ref, hat_i_cross

    def get_polarization_matrix(self):
        sp = np.sin(self.mesh_phi)
        cp = np.cos(self.mesh_phi)
        st = np.sin(self.mesh_theta)
        ct = np.cos(self.mesh_theta)

        a_11 = 1 - st * st * cp * cp
        a_12 = -st * st * sp * cp
        a_13 = -st * ct * cp
        a_21 = -st * st * sp * cp
        a_22 = 1 - st * st * sp * sp
        a_23 = -st * ct * sp
        a_31 = -st * ct * cp
        a_32 = -st * ct * sp
        a_33 = 1 - ct * ct
        matrix = np.array(
            [
                [a_11, a_12, a_13],
                [a_21, a_22, a_23],
                [a_31, a_32, a_33],
            ]
        )
        return matrix.swapaxes(0, 2).swapaxes(1, 3)

    def calculate_reference_fields(self):
        F = (
            np.array([self.Fx, self.Fy, self.Fz])
            .swapaxes(0, 1)
            .swapaxes(1, 2)
        )
        polarization_matrix = self.get_polarization_matrix()
        E = np.squeeze(polarization_matrix @ F[:, :, :, np.newaxis])

        hat_i_ref, hat_i_cross = self.get_reference_polarization()

        self.Fref[:, :] = np.multiply(E, hat_i_ref).sum(2)
        self.Fcross[:, :] = np.multiply(E, hat_i_cross).sum(2)

    def evaluate_local_field(self):
        self.local_field_flag = False

        self.local_Fphi = np.zeros(self.local_shape)
        self.local_Ftheta = np.zeros(self.local_shape)

        if self.evaluate_as == "isotropic":
            if self.evaluation_arguments["isotropic on"] == "both":
                self.local_Ftheta[:] = 0.7071067811865475  # 1/sqrt(2)
                self.local_Fphi[:] = 0.7071067811865475  # 1/sqrt(2)
            elif self.evaluation_arguments["isotropic on"] == "theta":
                self.local_Ftheta[:] = 1
                self.local_Fphi[:] = 0
            elif self.evaluation_arguments["isotropic on"] == "phi":
                self.local_Ftheta[:] = 0
                self.local_Fphi[:] = 1
        elif self.evaluate_as == "ideal dipole":
            if "dipole length" in self.evaluation_arguments.keys():
                self.ideal_dipole(
                    self.evaluation_arguments["dipole length"]
                )
            else:
                raise Exception(
                    "Tried to calculate ideal dipole "
                    + "field without dipole length."
                )
        if self.evaluate_as == "ideal loop dipole":
            if "loop dipole area" in self.evaluation_arguments.keys():
                self.ideal_loop_dipole(
                    self.evaluation_arguments["loop dipole area"]
                )
            else:
                raise Exception(
                    "Tried to calculate ideal dipole "
                    + "field without dipole length."
                )
        elif self.evaluate_as == "load file":
            if "file path" in self.evaluation_arguments.keys():
                self.load_file(self.evaluation_arguments["file path"])
            else:
                raise Exception(
                    "Tried to load file " + "without file path."
                )
        elif self.evaluate_as == "expressions":
            if (
                "expression theta" in self.evaluation_arguments.keys()
                and "expression phi"
                in self.evaluation_arguments.keys()
            ):
                self.eval_expression(
                    self.evaluation_arguments["expression theta"],
                    self.evaluation_arguments["expression phi"],
                )
            else:
                raise Exception(
                    "Tried to evaluate expression "
                    + "without expression."
                )

        a = np.absolute(self.local_Fphi)
        b = np.absolute(self.local_Ftheta)
        self.local_F = np.sqrt(a * a + b * b)
        
        # Normalize local fields
        max_magF = np.max(self.local_F)
        if max_magF > 1e-14:
            self.local_F = self.local_F / max_magF
            self.local_Ftheta = self.local_Ftheta / max_magF
            self.local_Fphi = self.local_Fphi / max_magF

    def evaluate(self):
        if self.ok:
            return

        t0 = time.time()

        if self.local_mesh_flag:
            self.evaluate_local_mesh()
        if self.R_flag:
            self.evaluate_R()
        if self.Rtheta_flag:
            self.evaluate_Rtheta()
        if self.Rphi_flag:
            self.evaluate_Rphi()
        if self.hats_flag:
            self.evaluate_hats()
        if self.local_field_flag:
            self.evaluate_local_field()
        if self.LG_interp_mesh_flag:
            self.evaluate_LG_interp_mesh()

        fit_points = (self.local_theta, self.local_phi)
        interp_points = (
            self.GL_interp_mesh_theta,
            self.GL_interp_mesh_phi,
        )

        values = self.local_Ftheta.copy()
        if values.dtype == np.dtype("complex64"):
            values = np.array(values, dtype=np.dtype("complex128"))
        interp = RegularGridInterpolator(
            fit_points, values, method="linear"
        )
        Ftheta = interp(interp_points)

        values = self.local_Fphi.copy()
        if values.dtype == np.dtype("complex64"):
            values = np.array(values, dtype=np.dtype("complex128"))
        interp = RegularGridInterpolator(
            fit_points, values, method="linear"
        )
        Fphi = interp(interp_points)

        self.Ftheta = Ftheta * (
            self.LG_interp_hat_theta * self.hat_theta
        ).sum(2) + Fphi * (
            self.LG_interp_hat_phi * self.hat_theta
        ).sum(
            2
        )
        self.Fphi = Ftheta * (
            self.LG_interp_hat_theta * self.hat_phi
        ).sum(2) + Fphi * (self.LG_interp_hat_phi * self.hat_phi).sum(
            2
        )

        a = np.absolute(self.Fphi)
        b = np.absolute(self.Ftheta)
        self.F = np.sqrt(a * a + b * b)
        
        # Normalize fields
        max_F = np.max(self.F)
        if max_F>1e-14:
            self.Ftheta = self.Ftheta/max_F
            self.Fphi = self.Fphi/max_F
            self.F = self.F/max_F

        # Circular polarization
        self.Frhcp = (self.Ftheta - 1j * self.Fphi) / MyMath.sqrt2
        self.Flhcp = (self.Ftheta + 1j * self.Fphi) / MyMath.sqrt2

        # Cartesian components fields
        vector_F = (
            self.Ftheta[:, :, np.newaxis] * self.hat_theta
            + self.Fphi[:, :, np.newaxis] * self.hat_phi
        )
        self.Fx = vector_F[:, :, 0]
        self.Fy = vector_F[:, :, 1]
        self.Fz = vector_F[:, :, 2]

        # Reference and Cross fields
        self.calculate_reference_fields()

        self.evaluation_time = time.time() - t0
        self.ok = True
        self.mark_update("evaluated")

    def ideal_dipole(self, L):
        st = np.sin(self.local_mesh_theta)
        ids = st != 0

        A = constants["k"] * L * constants["lam"] / 2

        self.local_Ftheta[ids] = (
            np.cos(A * np.cos(self.local_mesh_theta[ids])) - np.cos(A)
        ) / st[ids]

    def ideal_loop_dipole(self, S):
        pass

    def load_file(self, file_path):
        with open(file_path, "r") as f:
            reader = csv.reader(f)

            variations = []
            phi = []
            theta = []
            rEphi = []
            rEtheta = []

            self.header = reader.__next__()
            for line in reader:
                variations.append(line[0])
                phi.append(float(line[1]))
                theta.append(float(line[2]))
                a = line[3].split()
                rEphi.append(float(a[0]) * np.exp(1j * float(a[1])))
                a = line[4].split()
                rEtheta.append(float(a[0]) * np.exp(1j * float(a[1])))

            phi = np.array(phi)
            theta = np.array(theta)
            Fphi = (
                4
                * np.pi
                * np.array(rEphi)
                / (1j * constants["eta"] * constants["k"])
            )
            Ftheta = (
                4
                * np.pi
                * np.array(rEtheta)
                / (1j * constants["eta"] * constants["k"])
            )
            idsphi = theta == theta[0]
            idstheta = phi == phi[0]
            phi = phi[idsphi]
            theta = theta[idstheta]
            if self.evaluation_arguments["load mesh from file"]:
                self.local_phi = phi
                self.local_theta = theta
                self.local_mesh_flag = True
                self.local_shape = (
                    self.local_theta.size,
                    self.local_phi.size,
                )

                self.local_Fphi = np.reshape(
                    Fphi, (theta.size, phi.size)
                )
                self.local_Ftheta = np.reshape(
                    Ftheta, (theta.size, phi.size)
                )
            else:
                fit_points = (theta, phi)
                interp_points = (
                    self.local_mesh_theta,
                    self.local_mesh_phi,
                )

                values = np.reshape(Ftheta, (theta.size, phi.size))
                interp = RegularGridInterpolator(
                    fit_points, values, method="linear"
                )
                self.local_Ftheta = interp(interp_points)

                values = np.reshape(Fphi, (theta.size, phi.size))
                interp = RegularGridInterpolator(
                    fit_points, values, method="linear"
                )
                self.local_Fphi = interp(interp_points)

            self.evaluation_arguments["loaded file"] = file_path
            self.evaluation_arguments["force reload"] = False

    def eval_expression(self, expression_theta, expression_phi):
        new_vars = {
            "L": self.evaluation_arguments["dipole length"],
            "S": self.evaluation_arguments["loop dipole area"],
            "theta": self.local_mesh_theta,
            "phi": self.local_mesh_phi,
            "mesh_theta": self.local_mesh_theta,
            "mesh_phi": self.local_mesh_phi,
        }
        for key in constants.keys():
            new_vars[key] = constants[key]
        self.local_Ftheta = NEP.eval(
            expression=expression_theta, variables=new_vars
        )
        self.local_Fphi = NEP.eval(
            expression=expression_phi, variables=new_vars
        )
        self.local_Ftheta = np.broadcast_to(
            self.local_Ftheta, self.local_shape
        )
        self.local_Fphi = np.broadcast_to(
            self.local_Fphi, self.local_shape
        )

    def interpolate_at(
        self, interp_mesh_theta_deg, interp_mesh_phi_deg, field
    ):
        fit_points = (self.theta, self.phi)
        interp_points = (interp_mesh_theta_deg, interp_mesh_phi_deg)

        values = field
        if values.dtype == np.dtype("complex64"):
            values = np.array(values, dtype=np.dtype("complex128"))
        interp = RegularGridInterpolator(
            fit_points, values, method="linear"
        )
        interp_field = interp(interp_points)

        return interp_field

    def copy(self):
        antenna = Antenna(
            constants=constants,
            name=self.name,
            current_magnitude=self.current_magnitude,
            current_phase=self.current_phase,
            phi=self.phi.copy(),
            theta=self.theta.copy(),
            elevation=self.elevation,
            azimuth=self.azimuth,
            roll=self.roll,
            x=self.x,
            y=self.y,
            z=self.z,
            evaluate_as=self.evaluate_as,
        )

        antenna.evaluation_arguments = (
            self.evaluation_arguments.copy()
        )

        antenna.evaluate()
        return antenna


if __name__ == "__main__":
    import tkinter as tk
    import math

    constants = dict()
    constants["c"] = 299792458  # m/s
    constants["f"] = 433e6  # Hz
    constants["eta"] = 120 * math.pi
    constants["lam"] = constants["c"] / constants["f"]  # m
    constants["w"] = 2 * math.pi * constants["f"]  # rad/s
    constants["k"] = 2 * math.pi / constants["lam"]  # rad/m

    antenna = Antenna(constants=constants, name="loaded antenna")
    antenna.evaluate_as = antenna.load_file
    root = tk.Tk()
    root.geometry("0x0")
    file_path = tk.filedialog.askopenfilename(parent=root)
    root.destroy()
    if file_path != "":
        antenna.evaluation_arguments["file path"] = file_path
        antenna.evaluation_arguments["force reload"] = False
        antenna.evaluation_arguments["load mesh from file"] = True
        antenna.evaluate()

    def export_to_file(self, filename):
        with open(filename, mode="wb") as f:
            pickle.dump(self, f)


def load_from_file(file_path, load_mesh_from_file=False, **kw):
    antenna = Antenna(**kw)
    antenna.set_evaluation_method("load file")
    antenna.evaluation_arguments["file path"] = file_path
    antenna.evaluate()

    return antenna